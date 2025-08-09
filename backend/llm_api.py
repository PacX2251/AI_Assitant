# backend/main.py
import os
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

# LangChain imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load env vars
load_dotenv(r"C:/assistant/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for vector DB and LLM
VECTOR_DB_PATH = "./chroma_db"
retriever = None
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)


# Function to process uploaded files and create embeddings
def process_files_and_create_db(files_dir: str):
    loaders = [
        DirectoryLoader(files_dir, glob="**/*.txt", loader_cls=TextLoader),
        DirectoryLoader(files_dir, glob="**/*.pdf", loader_cls=PyPDFLoader),
        DirectoryLoader(files_dir, glob="**/*.csv", loader_cls=CSVLoader),
    ]

    all_docs = []
    for loader in loaders:
        try:
            all_docs.extend(loader.load())
        except Exception as e:
            print(f"Could not load files: {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_docs)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=VECTOR_DB_PATH)
    return db.as_retriever(search_kwargs={"k": 5})


@app.post("/upload_files")
async def upload_files(files: List[UploadFile]):
    os.makedirs("uploaded_files", exist_ok=True)
    for file in files:
        file_path = f"uploaded_files/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

    global retriever
    retriever = process_files_and_create_db("uploaded_files")

    return {"status": "Files processed and database updated"}


@app.post("/chat")
async def chat(message: str = Form(...)):
    if retriever is None:
        return {"error": "No documents uploaded yet."}

    docs = retriever.get_relevant_documents(message)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""You are an AI assistant. Use the following context to answer:
    {context}

    Question: {message}
    Answer:"""

    response = llm.invoke(prompt)
    return {"response": response.content}
