from dataclasses import dataclass


@dataclass
class RelationshipState:
    familiarity: float = 0.0
    trust: float = 0.0
    interaction_count: int = 0
    preferred_style: str = "natural"


class RelationshipEngine:
    def __init__(self):
        self._states: dict[str, RelationshipState] = {}

    def state_for(self, user_id: str) -> RelationshipState:
        if user_id not in self._states:
            self._states[user_id] = RelationshipState()
        return self._states[user_id]

    def record_interaction(self, user_id: str) -> RelationshipState:
        state = self.state_for(user_id)
        state.interaction_count += 1
        state.familiarity = min(1.0, state.familiarity + 0.01)
        return state
