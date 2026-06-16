from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import async_session
from app.models.card import Card
from app.services.seed_data import SEED_CARDS

router = APIRouter(prefix="/api/seed", tags=["seed"])


@router.post("/install")
async def install_seed():
    async with async_session() as db:
        existing = await db.execute(select(Card).limit(1))
        if existing.scalar_one_or_none():
            return {"message": "种子数据已存在，跳过"}

        for cd in SEED_CARDS:
            card = Card(
                material_id=0,  # 种子数据无关联材料
                question=cd["question"],
                answer=cd["answer"],
                importance_score=cd["importance_score"],
            )
            db.add(card)
        await db.commit()
    return {"message": f"已安装{len(SEED_CARDS)}张种子卡片"}
