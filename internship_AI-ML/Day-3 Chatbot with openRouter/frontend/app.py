import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"


st.title("My Chatbot")
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        try:
            response = requests.post(
                BACKEND_URL,
                json={"session_id": st.session_state.session_id, "message": user_input},
                stream=True,
                timeout=60
            )
            if "session_id" not in st.session_state:
                st.session_state.session_id = None
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                full_text += chunk
                placeholder.write(full_text)
        except requests.exceptions.ConnectionError:
            full_text = "Cannot connect to backend. Is uvicorn running on port 8000?"
            placeholder.write(full_text)
        except Exception as e:
            full_text = f"Error: {str(e)}"
            placeholder.write(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})