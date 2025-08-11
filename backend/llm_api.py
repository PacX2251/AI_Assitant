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

load_dotenv(r'C:/assistant/.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setting app for intercomunication
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Embeddings and Vectors
VECTOR_DB_PATH = "./chroma_db"
vector_db = None


# Post Method for upload files
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    global vector_db
    docs = []
    temp_files = []

    try:
        for file in files:
            filename = file.filename.lower()
            suffix = os.path.splitext(filename)[1]

            if suffix == ".txt":
                loader = TextLoader(file.file)
                docs.extend(loader.load())

            elif suffix in [".csv", ".pdf"]:
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    shutil.copyfileobj(file.file, tmp)
                    tmp_path = tmp.name
                    temp_files.append(tmp_path)

                if suffix == ".csv":
                    loader = CSVLoader(tmp_path)
                elif suffix == ".pdf":
                    loader = PyPDFLoader(tmp_path)

                docs.extend(loader.load())

            else:
                continue

        if not docs:
            return {"message": "No supported files uploaded."}

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=VECTOR_DB_PATH)

        return {"message": f"Uploaded and processed {len(files)} file(s)."}
    finally:
        # Borra archivos temporales
        for path in temp_files:
            try:
                os.remove(path)
            except Exception:
                pass
            
SCRAPI_API_URL = "http://localhost:1337/api/ai-conversations"

def save_conversation(user_msg, bot_reply):
    data = {
        "data": {
            "user_message": user_msg,
            "bot_reply": bot_reply,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }
    response = requests.post(SCRAPI_API_URL, json=data)
    if response.status_code not in (200, 201):
        print("Failed to save conversation:", response.text)

@app.post("/chat")
async def chat(request: ChatRequest):
    global vector_db
    if not vector_db:
        return {"reply": "Please upload documents first."}

    message = request.message
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    context_docs = retriever.invoke(message)

    context = "\n".join([doc.page_content for doc in context_docs])

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=OPENAI_API_KEY)
    prompt = f"""
You are a helpful assistant. Use the following context to answer the user's question.
If the answer is not contained in the context and it is related to it, specify that the information is not contained in the context,
but assume or infer the possible answer, clarifying that the answer is inferred.

Context:
{context}

User question:
{message}
"""

    response = llm.invoke(prompt)
    bot_reply = response.content

    # Guardar conversación en Scrapi
    save_conversation(message, bot_reply)

    return {"reply": bot_reply}
