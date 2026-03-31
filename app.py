import streamlit as st
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# -----------------------------
# LOAD MODELS
# -----------------------------
@st.cache_resource
def load_models():
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    llm = pipeline("text-generation", model="gpt2", device=-1)
    return embed_model, llm

embed_model, generator = load_models()

# -----------------------------
# LOAD FAISS
# -----------------------------
@st.cache_resource
def load_faiss():
    index = faiss.read_index("faiss.index")
    with open("meta.pkl", "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

index, metadata_store = load_faiss()

# -----------------------------
# RETRIEVAL
# -----------------------------
def retrieve(query, k=3):
    query_vec = embed_model.encode([query])
    D, I = index.search(np.array(query_vec), k)

    results = []
    for idx in I[0]:
        if idx < len(metadata_store):
            results.append(metadata_store[idx])
    return results

# -----------------------------
# GENERATE RESPONSE
# -----------------------------
def generate_answer(query, docs):
    context = "\n".join([d["text"] for d in docs])

    prompt = f"""
Context:
{context}

Q: {query}
A:
"""

    result = generator(prompt, max_length=200, do_sample=True)
    return result[0]["generated_text"]

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="RAG Chatbot")

st.title("RAG Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask your question")

if st.button("Send") and query:
    docs = retrieve(query)
    response = generate_answer(query, docs)

    sources = [d["metadata"].get("file", "doc") for d in docs]

    st.session_state.history.append((query, response, sources))

# -----------------------------
# DISPLAY
# -----------------------------
for q, r, s in st.session_state.history:

    st.markdown(f"""
    <div style='background:#1e1e1e;padding:10px;border-radius:10px'>
    <b> You:</b><br>{q}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#262730;padding:10px;border-radius:10px'>
    <b> Answer:</b><br>{r}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("** Sources:**")
    for src in s:
        st.write(f"- {src}")

    st.markdown("---")