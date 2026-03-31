# 🤖 RAG Chatbot (NEC + Wattmonk)

## 🚀 Overview
This project is a Retrieval-Augmented Generation (RAG) chatbot that answers queries from:
- NEC Electrical Code Guidelines
- Wattmonk Company Information
- General knowledge queries

It intelligently routes queries and retrieves relevant context before generating responses.

---

## 🧠 Features
- Multi-context query handling (NEC, Wattmonk, General)
- FAISS-based semantic search
- Context-aware response generation
- Conversation memory
- Source attribution (document citations)
- Confidence scoring
- Clean Streamlit UI

---

## 🏗️ Architecture
- Frontend: Streamlit
- Backend: Integrated into Streamlit
- LLM: GPT2 (local, free)
- Embeddings: Sentence Transformers
- Vector DB: FAISS

---

## 🔄 Workflow
1. User inputs query
2. Query processed and embedded
3. FAISS retrieves relevant documents
4. Context passed to LLM
5. Response generated with sources

---

## 📁 Project Structure
