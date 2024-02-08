# First
from langchain.llms import HuggingFaceHub
import os
import streamlit as st
with st.sidebar:
    hf_key = st.text_input("HuggingFace API Key", key="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", type="password")

st.title("💬 Chatbot") if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not hf_key:
        st.info("Please add your HuggingFace API key to continue.")
        st.stop()

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    llm = HuggingFaceHub(
    repo_id="huggingfaceh4/zephyr-7b-alpha",
    model_kwargs={"temperature": 0.5, "max_length": 64,"max_new_tokens":512}
)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
