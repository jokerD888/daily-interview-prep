from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.material import Material, MaterialStatus
from app.models.card import Card
from app.services.card_generator import get_card_generator

router = APIRouter(prefix="/api/materials", tags=["card-generation"])


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
