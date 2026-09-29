from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app.services.agent import Agent
from app.services.memory import MemoryStore
from app.services.relationship import RelationshipEngine

memory = MemoryStore()
relationship = RelationshipEngine()
agent = Agent(memory=memory, relationship=relationship)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await memory.connect()
    yield
    await memory.close()


app = FastAPI(title="Companion X API", version="0.2.0", lifespan=lifespan)


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "companion-x"}


@app.get("/health/memory")
async def memory_health():
    await memory.connect()
    return {"status": "ok", "service": "memory", "backend": "postgresql+pgvector"}


@app.post("/v1/chat")
async def chat(request: ChatRequest):
    result = await agent.respond(request.user_id, request.message)
    return result
