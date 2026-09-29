from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol
import os

import asyncpg


@dataclass
class Memory:
    user_id: str
    kind: str
    content: str
    importance: float = 0.5
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: int | None = None


class MemoryStoreProtocol(Protocol):
    async def remember(self, memory: Memory) -> None: ...
    async def recall(self, user_id: str, query: str, limit: int = 8) -> list[Memory]: ...


class MemoryStore:
    """Durable PostgreSQL memory store.

    PostgreSQL + pgvector is the persistence boundary. Until an embedding provider
    is configured, recall uses PostgreSQL full-text search plus importance/recentness.
    The schema already reserves a vector column for semantic retrieval.
    """

    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://companion:companion@localhost:5432/companion",
        ).replace("postgresql+asyncpg://", "postgresql://")
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=5)
            await self._init_schema()

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def _init_schema(self) -> None:
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute("""
                CREATE EXTENSION IF NOT EXISTS vector;
                CREATE TABLE IF NOT EXISTS memories (
                    id BIGSERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance DOUBLE PRECISION NOT NULL DEFAULT 0.5,
                    embedding vector(1536),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS memories_user_created_idx
                    ON memories(user_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS memories_user_kind_idx
                    ON memories(user_id, kind);
            """)

    async def remember(self, memory: Memory) -> None:
        await self.connect()
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO memories (user_id, kind, content, importance, created_at)
                VALUES ($1, $2, $3, $4, $5)
                """,
                memory.user_id,
                memory.kind,
                memory.content,
                memory.importance,
                memory.created_at,
            )

    async def recall(self, user_id: str, query: str, limit: int = 8) -> list[Memory]:
        await self.connect()
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, user_id, kind, content, importance, created_at,
                       ts_rank_cd(to_tsvector('simple', content),
                                  plainto_tsquery('simple', $2)) AS rank
                FROM memories
                WHERE user_id = $1
                ORDER BY
                    CASE WHEN $2 <> '' THEN rank ELSE 0 END DESC,
                    importance DESC,
                    created_at DESC
                LIMIT $3
                """,
                user_id,
                query,
                limit,
            )
        return [
            Memory(
                id=row["id"],
                user_id=row["user_id"],
                kind=row["kind"],
                content=row["content"],
                importance=row["importance"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
