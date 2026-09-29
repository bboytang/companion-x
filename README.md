# Companion X

A production-oriented AI companion platform: persistent memory, relationship continuity, proactive behavior, realtime voice, and avatar-ready clients.

## Current milestone

The backend now uses PostgreSQL + pgvector for durable memory. Memory records survive API restarts and are retrieved with vector similarity, importance, and recency.

## Architecture

User -> API -> Agent -> Memory / Relationship -> Planner -> Actions -> Voice / Avatar

## Development

Python 3.12+ is recommended.

1. Copy environment settings from .env.example to .env.
2. Start PostgreSQL + pgvector and Redis with docker compose.
3. Install the backend package.
4. Start FastAPI.

Health endpoint: GET /health

## Memory

The memories table stores durable conversation/event/fact records and a 1536-dimensional vector. The EmbeddingProvider is an adapter boundary; the current local implementation is deterministic and dependency-free so development works without a model API key. It can later be replaced by a production embedding model without changing the memory API.

## Principles

1. Memory is a product primitive, not prompt stuffing.
2. Proactive behavior must have a reason and a cooldown.
3. The agent is independent from avatar and voice providers.
4. Every external provider is behind an adapter interface.
5. The mobile client can start as a browser client and later become native iOS/Android.
