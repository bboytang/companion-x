from datetime import datetime, timezone

from app.services.memory import Memory, MemoryStoreProtocol
from app.services.relationship import RelationshipEngine


class Agent:
    def __init__(self, memory: MemoryStoreProtocol, relationship: RelationshipEngine):
        self.memory = memory
        self.relationship = relationship

    async def respond(self, user_id: str, message: str) -> dict:
        recalled = await self.memory.recall(user_id, message)
        state = self.relationship.record_interaction(user_id)

        # Provider-independent placeholder. Real model adapters will plug in here.
        reply = f"收到。你刚才说的是：{message}"

        await self.memory.remember(
            Memory(
                user_id=user_id,
                kind="conversation",
                content=message,
                importance=0.2,
            )
        )

        return {
            "reply": reply,
            "memory_context": [m.content for m in recalled],
            "relationship": {
                "familiarity": state.familiarity,
                "trust": state.trust,
                "interaction_count": state.interaction_count,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
