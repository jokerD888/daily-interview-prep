from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.material import Material, MaterialStatus
from app.models.card import Card
from app.models.card_progress import CardProgress, CardState
from app.services.card_generator import get_card_generator
from app.schemas.bridge import BulkImportRequest, BulkImportResponse

router = APIRouter(prefix="/api/materials", tags=["card-generation"])

# --- card bridge ---
card_router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.post("/{material_id}/generate", status_code=202)
async def generate_cards(
    material_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Material).where(Material.id == material_id, Material.user_id == user.id)
    )
    material = result.scalar_one_or_none()
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资料不存在")
    if not material.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="资料内容为空")

    material.status = MaterialStatus.processing
    await db.commit()

    try:
        generator = get_card_generator()
        cards_data = await generator.generate_cards(material.content)
        for cd in cards_data:
            card = Card(
                material_id=material.id,
                question=cd["question"],
                answer=cd["answer"],
                importance_score=int(cd.get("importance_score", 1)),
            )
            db.add(card)
        material.status = MaterialStatus.completed
    except Exception:
        material.status = MaterialStatus.failed
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="卡片生成失败，请重试")

    await db.commit()
    return {"message": f"成功生成{len(cards_data)}张卡片", "card_count": len(cards_data)}


@router.get("/{material_id}/cards")
async def get_material_cards(
    material_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Material).where(Material.id == material_id, Material.user_id == user.id)
    )
    material = result.scalar_one_or_none()
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="资料不存在")

    card_result = await db.execute(
        select(Card).where(Card.material_id == material_id)
    )
    cards = card_result.scalars().all()
    return [{"id": c.id, "question": c.question, "answer": c.answer, "importance_score": c.importance_score} for c in cards]


# --- /api/cards/bulk-import (bridge from InterviewLens) ---

@card_router.post("/bulk-import", response_model=BulkImportResponse)
async def bulk_import(
    req: BulkImportRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Import cards from external systems (InterviewLens bridge).

    Each card is inserted with scheduler_state="new" and enters the daily queue.
    Duplicates are detected by (user_id, question) and skipped.
    """
    imported = 0
    skipped = 0
    skipped_reasons: list[str] = []

    # Fetch existing question texts for this user in one query.
    existing_q = (
        await db.execute(
            select(Card.question).join(CardProgress).where(
                CardProgress.user_id == user.id,
                CardProgress.card_id == Card.id,
            )
        )
    ).scalars().all()
    existing_set = set(existing_q)

    from datetime import datetime

    for item in req.cards:
        if item.question in existing_set:
            skipped += 1
            skipped_reasons.append(f"问题重复: '{item.question[:40]}'")
            continue

        card = Card(
            material_id=None,
            question=item.question,
            answer=item.answer,
            importance_score=item.importance_score,
            source_url=item.source_url,
        )
        db.add(card)
        await db.flush()  # get card.id

        progress = CardProgress(
            user_id=user.id,
            card_id=card.id,
            state=CardState.new.value,
            next_review_at=datetime.utcnow(),
        )
        db.add(progress)
        existing_set.add(item.question)
        imported += 1

    await db.commit()
    return BulkImportResponse(imported=imported, skipped=skipped, skipped_reasons=skipped_reasons)
