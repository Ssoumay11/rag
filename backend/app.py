from fastapi import FastAPI
from backend.routes.chat import router as chat_router

app = FastAPI(title="RAG Chatbot")

app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running 🚀"}