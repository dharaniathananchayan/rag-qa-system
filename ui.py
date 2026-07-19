import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖"
)

st.title("📚 RAG PDF Chatbot")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    if st.button("Upload PDF"):

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        st.success("PDF uploaded successfully!")

        st.json(response.json())

# Ask Question
if "messages" not in st.session_state:
    st.session_state.messages = []

question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = requests.post(
        f"{API_URL}/ask",
        params={"question": question}
    )

    answer = response.json()["answer"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])