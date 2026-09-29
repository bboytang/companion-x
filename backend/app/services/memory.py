from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol


@dataclass
class Memory:
    user_id: str
    kind: str
    content: str
    importance: float = 0.5
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryStoreProtocol(Protocol):
    async def remember(self, memory: Memory) -> None: ...
    async def recall(self, user_id: str, query: str, limit: int = 8) -> list[Memory]: ...


class MemoryStore:
    """Temporary in-process implementation.

    This interface will be backed by PostgreSQL + pgvector in the next layer.
    """

    def __init__(self):
        self._items: list[Memory] = []

    async def remember(self, memory: Memory) -> None:
        self._items.append(memory)

    async def recall(self, user_id: str, query: str, limit: int = 8) -> list[Memory]:
        items = [m for m in self._items if m.user_id == user_id]
        return sorted(items, key=lambda m: m.importance, reverse=True)[:limit]
