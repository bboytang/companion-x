CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS memories (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    content TEXT NOT NULL,
    importance DOUBLE PRECISION NOT NULL DEFAULT 0.5,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    embedding VECTOR(1536)
);

CREATE INDEX IF NOT EXISTS memories_user_created_idx
    ON memories (user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS memories_user_kind_idx
    ON memories (user_id, kind);

CREATE INDEX IF NOT EXISTS memories_embedding_hnsw_idx
    ON memories USING hnsw (embedding vector_cosine_ops);
