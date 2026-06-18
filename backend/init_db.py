"""Initialize DB schema. Run once: python init_db.py"""
import asyncio
from app.models.base import Base
from app.models import User, Material, Card, CardProgress, ReviewLog  # noqa
from app.core.database import engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # bridge migrations (safe to re-run — SQLite ADD COLUMN IF NOT EXISTS)
        await conn.run_sync(
            lambda sync_conn: sync_conn.exec_driver_sql(
                "ALTER TABLE cards ADD COLUMN source_url TEXT"
            )
        )  # ponytail: IF NOT EXISTS not supported in SQLite, ignore error on re-run


if __name__ == "__main__":
    asyncio.run(init_db())
