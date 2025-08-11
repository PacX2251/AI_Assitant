import os
import tempfile
import shutil
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime, timezone

# Load API key from .env file
load_dotenv(r'C:/assistant/.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Global variables for session persistence
VECTOR_DB_PATH = "./chroma_db"
vector_db = None
uploaded_filenames = []  # Will store all uploaded filenames in current session

# Reset ChromaDB and file list when backend starts
if os.path.exists(VECTOR_DB_PATH):
    shutil.rmtree(VECTOR_DB_PATH)
vector_db = None
uploaded_filenames.clear()

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Handles file uploads, processes them, and stores embeddings in ChromaDB.
    This function supports .txt, .csv, and .pdf formats.
    The vector DB persists until the session is reset (e.g., page reload).
    """
    global vector_db

    supported_ext = [".txt", ".csv", ".pdf"]
    docs = []
    temp_files = []

    uploaded_filenames = []  # List to send back to frontend

    try:
        for file in files:
            filename = file.filename
            uploaded_filenames.append(filename)
            suffix = os.path.splitext(filename.lower())[1]

            # Skip unsupported formats
            if suffix not in supported_ext:
                continue

            # Save uploaded file to a temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
                temp_files.append(tmp_path)

            # Load documents depending on file type
            if suffix == ".txt":
                loader = TextLoader(tmp_path, encoding="utf-8")
            elif suffix == ".csv":
                loader = CSVLoader(tmp_path)
            elif suffix == ".pdf":
                loader = PyPDFLoader(tmp_path)

            docs.extend(loader.load())

        if not docs:
            return {"message": "No supported files uploaded.", "files": []}

        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        # Create or update ChromaDB
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        if vector_db is None:
            vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=VECTOR_DB_PATH)
        else:
            vector_db.add_documents(chunks)

        return {
            "message": f"Uploaded and processed {len(uploaded_filenames)} file(s).",
            "files": uploaded_filenames
        }

    finally:
        # Remove temp files
        for path in temp_files:
            try:
                os.remove(path)
            except Exception:
                pass

# Strapi API endpoint to save conversations
SCRAPI_API_URL = "http://localhost:1337/api/ai-conversations"

def save_conversation(user_msg, bot_reply):
    """
    Save each conversation exchange to Strapi.
    """
    data = {
        "data": {
            "user_message": user_msg,
            "bot_reply": bot_reply,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }
    try:
        response = requests.post(SCRAPI_API_URL, json=data)
        if response.status_code not in (200, 201):
            print("Failed to save conversation:", response.text)
    except Exception as e:
        print("Error saving conversation:", e)

@app.post("/chat")
async def chat(request: ChatRequest):
    global vector_db
    if not vector_db:
        return {"reply": "Please upload documents first."}

    message = request.message

    retriever = vector_db.as_retriever(search_kwargs={"k": 10})
    context_docs = retriever.get_relevant_documents(message)
    context = "\n".join([doc.page_content for doc in context_docs])

    print("=== Contexto recuperado para la pregunta ===")
    for i, doc in enumerate(context_docs):
        print(f"Doc {i+1}:\n{doc.page_content}\n{'-'*40}")

    prompt = f"""

You are a knowledgeable and helpful assistant. Your main purpose is to answer the user's question using the provided context below.

- If the answer is explicitly found in the context, answer based strictly on that information.
- If the answer is not present in the context but is related, clearly state that the information is not directly available, then provide a well-reasoned inference or assumption based on the context. Make sure to explicitly mention that your answer is inferred.
- If the question is unrelated to the context, politely inform the user that you don't have enough information to answer.

Context:
{context}

User question:
{message}
"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, openai_api_key=OPENAI_API_KEY)
    response = llm.invoke(prompt)
    bot_reply = response.content

    save_conversation(message, bot_reply)

    return {"reply": bot_reply}
