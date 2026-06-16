from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.card import Card
from app.models.card_progress import CardProgress, CardState, ReviewResult, ReviewLog
from app.services.scheduler import advance_state, reset_state

router = APIRouter(prefix="/api", tags=["review"])


@router.get("/daily-cards")
async def get_daily_cards(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    now = datetime.utcnow()

    # Due review cards
    review_query = (
        select(CardProgress)
        .options(joinedload(CardProgress.card))
        .where(
            and_(
                CardProgress.user_id == user.id,
                CardProgress.next_review_at <= now,
                CardProgress.state != CardState.mastered.value,
            )
        )
        .order_by(CardProgress.next_review_at.asc())
    )
    result = await db.execute(review_query)
    due_reviews = result.unique().scalars().all()

    total_quota = settings.DAILY_NEW_CARDS + settings.DAILY_REVIEW_CARDS
    cards_response = []

    # Review cards first
    for cp in due_reviews[:total_quota]:
        cards_response.append(_card_progress_to_dict(cp))

    # Fill with new cards
    remaining = max(0, total_quota - len(cards_response))
    if remaining > 0:
        learned_ids = set()
        learned_result = await db.execute(
            select(CardProgress.card_id).where(CardProgress.user_id == user.id)
        )
        learned_ids = {r[0] for r in learned_result.all()}

        new_query = (
            select(Card)
            .where(~Card.id.in_(learned_ids) if learned_ids else True)
            .order_by(Card.importance_score.desc())
            .limit(remaining)
        )
        new_result = await db.execute(new_query)
        for card in new_result.scalars().all():
            cards_response.append({
                "card_id": card.id,
                "question": card.question,
                "answer": card.answer,
                "importance_score": card.importance_score,
                "state": "new",
            })

    return cards_response


@router.post("/reviews")
async def submit_review(
    card_id: int,
    result: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if result not in ("correct", "forgot"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="result must be 'correct' or 'forgot'")

    result_enum = ReviewResult.correct if result == "correct" else ReviewResult.forgot

    progress_result = await db.execute(
        select(CardProgress).where(
            and_(CardProgress.user_id == user.id, CardProgress.card_id == card_id)
        )
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        progress = CardProgress(user_id=user.id, card_id=card_id, state=CardState.new.value)
        db.add(progress)
        await db.flush()

    current_state = CardState(progress.state)
    if result_enum == ReviewResult.correct:
        new_state, next_review = advance_state(current_state)
    else:
        new_state, next_review = reset_state()

    progress.state = new_state.value
    progress.next_review_at = next_review

    log = ReviewLog(user_id=user.id, card_id=card_id, result=result_enum.value)
    db.add(log)
    await db.commit()

    return {"state": new_state.value, "next_review_at": next_review.isoformat()}


def _card_progress_to_dict(cp: CardProgress) -> dict:
    return {
        "card_id": cp.card.id,
        "question": cp.card.question,
        "answer": cp.card.answer,
        "importance_score": cp.card.importance_score,
        "state": cp.state,
        "next_review_at": cp.next_review_at.isoformat() if cp.next_review_at else None,
    }
