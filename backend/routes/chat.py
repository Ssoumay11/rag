from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.classifier import classify_query
from backend.services.rag_pipeline import rag_response
from backend.services.llm import general_response
from backend.services.memory import update_memory

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
def chat(req: ChatRequest):
    query = req.query

    intent = classify_query(query)

    if intent == "general":
        response = general_response(query)
        sources = []
        confidence = 0.5
    else:
        response, sources, confidence = rag_response(query, intent)

    update_memory(query, response)

    return {
        "response": response,
        "intent": intent,
        "sources": sources,
        "confidence": confidence
    }