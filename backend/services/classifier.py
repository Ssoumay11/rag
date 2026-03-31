def classify_query(query: str) -> str:
    q = query.lower()

    if "nec" in q or "electrical" in q:
        return "nec"
    elif "wattmonk" in q or "company" in q:
        return "wattmonk"
    else:
        return "general"