from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from app.db import close_pool, create_pool
from app.services.agent import Agent
from app.services.embeddings import EmbeddingProvider
from app.services.memory import PostgresMemoryStore
from app.services.relationship import RelationshipEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_pool()
    app.state.db_pool = pool
    app.state.memory = PostgresMemoryStore(pool, EmbeddingProvider())
    app.state.relationship = RelationshipEngine()
    app.state.agent = Agent(app.state.memory, app.state.relationship)
    yield
    await close_pool(pool)

app = FastAPI(title="Companion X API", version="0.2.0", lifespan=lifespan)

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.get("/health")
async def health():
    await app.state.db_pool.fetchval("SELECT 1")
    return {"status": "ok", "service": "companion-x", "memory": "postgres-pgvector"}

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    return await app.state.agent.respond(request.user_id, request.message)
