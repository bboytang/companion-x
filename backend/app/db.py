import asyncpg
from app.config import settings

def _dsn() -> str:
    return settings.database_url.replace("postgresql+asyncpg://", "postgresql://", 1)

async def create_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(_dsn(), min_size=1, max_size=5)

async def close_pool(pool: asyncpg.Pool) -> None:
    await pool.close()
