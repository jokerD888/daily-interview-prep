import asyncio
from app.models.base import Base
from app.models import User, Material, Card, CardProgress, ReviewLog  # noqa
from app.core.database import engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
