import streamlit as st
from langchain.llms import HuggingFaceHub
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Set up Hugging Face token
HF_TOKEN = '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'
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN

# Load PDF documents
loader = PyPDFDirectoryLoader("pdfs")
loader.requests_per_second = 1
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
chunks = text_splitter.split_documents(docs)

# Create vector store
vectorstore = Chroma.from_documents(chunks, persist_directory="db")

# Create retriever
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 4})

# Set up language model
llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    model_kwargs={"temperature": 0.5, "max_length": 64, "max_new_tokens": 512}
)

# Create Streamlit app
st.title("Chat with AI")

# Define system prompt
DEFAULT_SYSTEM_PROMPT = """
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
""".strip()

# Define Streamlit chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.expander(message["role"]):
        st.write(message["content"])

if prompt := st.text_input("User:"):
    st.session_state.messages.append({"role": "User", "content": prompt})

    # Generate response
    query = prompt
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever)
    response = qa.run(DEFAULT_SYSTEM_PROMPT)
    st.session_state.messages.append({"role": "AI", "content": response})
