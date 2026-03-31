import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="RAG Chatbot", layout="centered")

st.title(" RAG Chatbot")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
query = st.text_input("Ask your question")

# Send button
if st.button("Send") and query:
    try:
        res = requests.post(API_URL, json={"query": query}).json()
        st.session_state.history.append((query, res))
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

# Display chat history
for q, r in st.session_state.history:
    
    # User message
    st.markdown(f"""
    <div style='background-color:#1e1e1e;padding:10px;border-radius:10px;margin-bottom:5px'>
    <b> You:</b><br>{q}
    </div>
    """, unsafe_allow_html=True)

    # Bot response
    st.markdown(f"""
    <div style='background-color:#262730;padding:10px;border-radius:10px;margin-bottom:5px'>
    <b> Answer:</b><br>{r['response']}
    </div>
    """, unsafe_allow_html=True)

    # Sources
    if r.get("sources"):
        st.markdown("** Sources:**")
        for s in r["sources"]:
            st.write(f"- {s}")

    # Confidence
    st.markdown(f"** Confidence:** {round(r.get('confidence', 0), 2)}")

    st.markdown("---")