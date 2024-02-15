from langchain.llms import HuggingFaceHub
from langchain.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import  Chroma
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA, LLMChain
import streamlit as st
st.title("Chatbot")

client = HuggingFaceHub(HF_key=st.secrets["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"])

if huggingface_model not in st.session_state:
    st.session_state[huggingface_model]="mistralai/Mixtral-8x7B-Instruct-v0.1",
    model_kwargs={"temperature": 0.5, "max_length": 64,"max_new_tokens":512}

if messages not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state[huggingface_model],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

