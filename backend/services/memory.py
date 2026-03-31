chat_history = []

def update_memory(query, response):
    chat_history.append({
        "query": query,
        "response": response
    })

def get_memory():
    return chat_history[-5:]