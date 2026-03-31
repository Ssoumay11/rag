from transformers import pipeline

# Load FLAN-T5 model (best free option)
generator = pipeline(
    "text-generation",
    model="google/flan-t5-small",
    device=-1  # CPU
)

def call_llm(prompt):
    try:
        result = generator(
            prompt,
            max_length=256,
            do_sample=False  # more stable answers
        )
        return result[0]["generated_text"]
    except Exception as e:
        return f"LLM Error: {str(e)}"


def general_response(query):
    return call_llm(f"Answer clearly:\n{query}")


def generate_rag_answer(query, context):
    prompt = f"""
Use the context to answer the question.

Context:
{context}

Question:
{query}

Give a short answer in bullet points:
"""
    return call_llm(prompt)