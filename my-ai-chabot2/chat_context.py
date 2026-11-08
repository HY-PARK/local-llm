import streamlit as st
import ollama

st.title("My Local AI Chatbot")

with st.sidebar:
    model = st.selectbox("Select a model:", ["gemma4:12b", "qwen3.8:27b"])

    max_history = st.slider("Max History", min_value=1, max_value=10, value=5)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if "message" in st.session_state:
        total_message = len(st.session_state.messages)
        total_chars = sum(len(msg["content"]) for msg in st.session_state.messages)
        st.divider()
        st.caption("Conversation Stats")
        st.metric("Messages", total_message)
        st.metric("Approx. Tokens", total_chars // 4)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    max_message = max_history * 2 + 1
    message_for_model = st.session_state.messages[-max_message:]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""
        stream = ollama.chat(
            model=model,
            messages=message_for_model,
            stream=True,
        )
        for chunk in stream:
            response_text += chunk["message"]["content"]
            placeholder.markdown(response_text + "▌")

        placeholder.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
