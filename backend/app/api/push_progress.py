from fastapi import APIRouter, Depends
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.card_progress import CardProgress, CardState, ReviewLog

router = APIRouter(prefix="/api", tags=["push", "progress"])

# ---- Push Subscriptions (stub – full implementation needs a PushSubscription model) ----

@router.post("/push-subscription")
async def subscribe_push(user: User = Depends(get_current_user)):
    return {"message": "Push subscription stub"}


@router.delete("/push-subscription")
async def unsubscribe_push(user: User = Depends(get_current_user)):
    return {"message": "Push unsubscription stub"}


# ---- Progress ----

@router.get("/progress")
async def get_progress(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Count cards by state
    state_query = (
        select(CardProgress.state, func.count(CardProgress.id))
        .where(CardProgress.user_id == user.id)
        .group_by(CardProgress.state)
    )
    state_result = await db.execute(state_query)
    state_counts = {r[0]: r[1] for r in state_result.all()}

    # Today's reviews
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_result = await db.execute(
        select(func.count(ReviewLog.id)).where(
            and_(ReviewLog.user_id == user.id, ReviewLog.reviewed_at >= today)
        )
    )
    today_reviewed = today_result.scalar() or 0

    # Streak calculation
    streak = await _calculate_streak(db, user.id)

    # Cards pending today
    pending_result = await db.execute(
        select(func.count(CardProgress.id)).where(
            and_(
                CardProgress.user_id == user.id,
                CardProgress.next_review_at <= datetime.utcnow(),
                CardProgress.state != CardState.mastered,
            )
        )
    )
    today_remaining = pending_result.scalar() or 0

    total = sum(state_counts.values())
    mastered = state_counts.get(CardState.mastered, 0)
    learning = total - mastered

    return {
        "total_cards": total,
        "mastered_count": mastered,
        "learning_count": learning,
        "new_count": state_counts.get(CardState.new, 0),
        "daily_streak": streak,
        "today_reviewed": today_reviewed,
        "today_remaining": today_remaining,
    }


@router.get("/progress/history")
async def get_progress_history(
    month: str = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not month:
        month = datetime.utcnow().strftime("%Y-%m")
    try:
        year, mon = int(month.split("-")[0]), int(month.split("-")[1])
    except (ValueError, IndexError):
        year, mon = datetime.utcnow().year, datetime.utcnow().month

    start = datetime(year, mon, 1)
    if mon == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, mon + 1, 1)

    result = await db.execute(
        select(
            func.date(ReviewLog.reviewed_at).label("date"),
            func.count(ReviewLog.id).label("count"),
        )
        .where(
            and_(
                ReviewLog.user_id == user.id,
                ReviewLog.reviewed_at >= start,
                ReviewLog.reviewed_at < end,
            )
        )
        .group_by("date")
    )
    return [{"date": str(r[0]), "review_count": r[1]} for r in result.all()]


async def _calculate_streak(db: AsyncSession, user_id: int) -> int:
    """Count consecutive days with reviews backwards from today."""
    streak = 0
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(366):
        check_date = today - timedelta(days=i)
        next_date = check_date + timedelta(days=1)
        result = await db.execute(
            select(func.count(ReviewLog.id)).where(
                and_(
                    ReviewLog.user_id == user_id,
                    ReviewLog.reviewed_at >= check_date,
                    ReviewLog.reviewed_at < next_date,
                )
            )
        )
        if result.scalar() > 0:
            streak += 1
        else:
            break
    return streak
