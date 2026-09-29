from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol
import asyncpg
from app.services.embeddings import EmbeddingProvider

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

class PostgresMemoryStore:
    """Durable memory backed by PostgreSQL + pgvector."""

    def __init__(self, pool: asyncpg.Pool, embeddings: EmbeddingProvider | None = None):
        self.pool = pool
        self.embeddings = embeddings or EmbeddingProvider()

    async def remember(self, memory: Memory) -> None:
        embedding = self.embeddings.embed(memory.content)
        vector_literal = "[" + ",".join(str(x) for x in embedding) + "]"
        await self.pool.execute(
            """INSERT INTO memories
               (user_id, kind, content, importance, created_at, embedding)
               VALUES ($1, $2, $3, $4, $5, $6::vector)""",
            memory.user_id, memory.kind, memory.content,
            memory.importance, memory.created_at, vector_literal,
        )

    async def recall(self, user_id: str, query: str, limit: int = 8) -> list[Memory]:
        embedding = self.embeddings.embed(query)
        vector_literal = "[" + ",".join(str(x) for x in embedding) + "]"
        rows = await self.pool.fetch(
            """SELECT id, user_id, kind, content, importance, created_at
               FROM memories
               WHERE user_id = $1
               ORDER BY embedding <=> $2::vector, importance DESC, created_at DESC
               LIMIT $3""",
            user_id, vector_literal, limit,
        )
        return [Memory(
            id=row["id"], user_id=row["user_id"], kind=row["kind"],
            content=row["content"], importance=row["importance"],
            created_at=row["created_at"],
        ) for row in rows]
