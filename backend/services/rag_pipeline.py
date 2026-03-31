from backend.services.retriever import retrieve_docs
from backend.services.llm import generate_rag_answer


def clean_response(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()
        if line and line not in cleaned:
            if not line.startswith("-"):
                line = "- " + line
            cleaned.append(line)

    return "\n".join(cleaned[:5])

def rag_response(query, source):
    docs, scores = retrieve_docs(query, source)

    if not docs:
        return "No relevant documents found.", [], 0.0

    context = "\n".join([d["text"] for d in docs[:3]])

    response = generate_rag_answer(query, context)

    response = clean_response(response)

    confidence = sum(scores) / len(scores) if scores else 0

    # ✅ Better citations
    sources = [
        f"{d['metadata'].get('file', 'doc')} (chunk {i})"
        for i, d in enumerate(docs[:3])
    ]

    return response, sources, confidence