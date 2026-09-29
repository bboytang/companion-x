# Companion X

A production-oriented AI companion platform: persistent memory, relationship continuity, proactive behavior, realtime voice, and avatar-ready clients.

## Architecture

User -> API -> Agent -> Memory / Relationship -> Planner -> Actions -> Voice / Avatar

### Services

- api: FastAPI HTTP/WebSocket boundary
- agent: model-agnostic reasoning and tool orchestration
- memory: durable user/event/episode/relationship memory
- relationship: continuity, preferences, interaction state
- proactive: scheduled/event-driven wakeups
- voice: STT/TTS/realtime voice adapter boundary
- avatar: Live2D/3D adapter boundary

## First milestone

The first commit intentionally contains interfaces and a runnable API skeleton rather than coupling the product to one model provider.

## Development

Python 3.12+ is recommended.

```bash
cp .env.example .env
docker compose up -d
```

API health: `GET /health`

## Principles

1. Memory is a product primitive, not prompt stuffing.
2. Proactive behavior must have a reason and a cooldown.
3. The agent is independent from avatar and voice providers.
4. Every external provider is behind an adapter interface.
5. The mobile client can start as a browser client and later become native iOS/Android.
