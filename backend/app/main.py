from fastapi import FastAPI
from pydantic import BaseModel

from app.services.agent import Agent
from app.services.memory import MemoryStore
from app.services.relationship import RelationshipEngine

app = FastAPI(title="Companion X API", version="0.1.0")

memory = MemoryStore()
relationship = RelationshipEngine()
agent = Agent(memory=memory, relationship=relationship)


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.get("/health")
async def health():
    return {"status": "ok", "service": "companion-x"}


@app.post("/v1/chat")
async def chat(request: ChatRequest):
    result = await agent.respond(request.user_id, request.message)
    return result
