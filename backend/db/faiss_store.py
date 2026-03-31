import faiss
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer
from backend.config import FAISS_INDEX_PATH

model = SentenceTransformer("all-MiniLM-L6-v2")

DIM = 384

if os.path.exists(FAISS_INDEX_PATH):
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open("backend/db/meta.pkl", "rb") as f:
        metadata_store = pickle.load(f)
else:
    index = faiss.IndexFlatL2(DIM)
    metadata_store = []

def add_documents(docs):
    texts = [d["text"] for d in docs]
    embeddings = model.encode(texts)

    index.add(np.array(embeddings))

    metadata_store.extend(docs)

    faiss.write_index(index, FAISS_INDEX_PATH)
    with open("backend/db/meta.pkl", "wb") as f:
        pickle.dump(metadata_store, f)

def search(query, k=5):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(metadata_store):
            results.append({
                "text": metadata_store[idx]["text"],
                "metadata": metadata_store[idx]["metadata"],
                "score": float(score)
            })

    return results