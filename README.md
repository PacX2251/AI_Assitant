# AI_Assitant
Building an AI-powered assistant with Retrieval-Augmented Generation (RAG) and tools.
Notion Link: https://www.notion.so/Mini-AI-Knowledge-Assistant-ActivaMente-Challenge-24a7dc188d0f80c78cd7d755eb03a3f5?source=copy_link

## Overview

This project is a Mini AI Assistant powered by Retrieval-Augmented Generation (RAG) and custom tools.  
Users can upload documents to create a knowledge base, chat with the assistant, and perform external actions via API integrations.  

## Repository Structure

```
ai-assistant
│
├── frontend
│   ├── public
│   ├── src
│   ├── package.json
│   └── README.md
│
├── backend
│   ├── api.py
│   ├── embedding.py
│   ├── tools.py
│   ├── db.py
│   ├── requirements.txt
│   └── README.md
│
├── database
│   ├── data_ingestion.py
│   └── README.md
│
├── cms
│   ├── strapi_integration.py
│   └── README.md
│
├── docs
│   ├── architecture_diagram.png
│   ├── DEPLOY.md
│   └── planning.md
│
└── README.md
```
- `frontend/`  
  React app for the chat interface and file uploads.

- `backend/`  
  FastAPI backend handling AI logic, embeddings, and API calls.

- `database/`  
  Scripts for data ingestion, cleaning, and storage in PostgreSQL.

- `cms/`  
  Integration scripts for Strapi CMS for notes and tasks management.

- `docs/`  
  Documentation, architecture diagrams, deployment instructions.

## Getting Started

### Frontend

1. Navigate to `frontend/`  
2. Run `npm install`  
3. Run `npm start` to launch the UI locally.

### Backend

1. Navigate to `backend/`  
2. Create and activate a Python virtual environment.  
3. Run `pip install -r requirements.txt`  
4. Run `uvicorn api:app --reload` to start the API server.

### Database

- Use `database/data_ingestion.py` to ingest and prepare data for the vector store and PostgreSQL.

### CMS

- Use `cms/strapi_integration.py` to interact with Strapi CMS for managing notes/tasks.

## Deployment

Please refer to `docs/DEPLOY.md` for deployment instructions.

## Contact

For questions, contact [your_email@example.com]
