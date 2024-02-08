import streamlit as st
import random
import time

from openai import OpenAI
import streamlit as st
from langchain.llms import HuggingFaceHub
from langchain.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import  Chroma
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA, LLMChain
import os

st.title("ChatGPT-like clone")


client= HuggingFaceHub(hf_key=st.secrets["HUGGINGFACEHUB_API_TOKEN"])
HF_TOKEN= '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'
#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

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
