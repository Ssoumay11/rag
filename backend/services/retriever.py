from backend.db.faiss_store import search

def retrieve_docs(query, source):
    results = search(query)

    filtered = [r for r in results if r["metadata"]["source"] == source]

    return filtered[:5], [r["score"] for r in filtered[:5]]