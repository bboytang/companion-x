# Companion X Architecture

## Runtime path

1. Client sends text or realtime audio.
2. API authenticates the session and normalizes the event.
3. Agent loads relevant memory and relationship state.
4. Planner determines whether to answer, use a tool, remember something, or schedule a future action.
5. Model adapter generates the response.
6. Voice/avatar adapters render the response.
7. Memory pipeline extracts durable facts/events/episodes after the turn.

## Memory layers

- User facts
- Events
- Conversation episodes
- Relationship memory
- Emotional trend
- Preferences and goals

## Proactive engine

Triggers are not messages. A trigger creates a candidate wake-up event.

The planner evaluates:
- reason to contact
- freshness
- relationship context
- user quiet hours
- cooldown
- confidence
- urgency

Only then can an action be emitted.

## Provider boundaries

LLM, STT, TTS, realtime voice, avatar, vector database, and notification providers must be replaceable adapters.
