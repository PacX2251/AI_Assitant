# AI_Assitant
Building an AI-powered assistant with Retrieval-Augmented Generation (RAG) and tools.

## Overview

This project is a Mini AI Assistant powered by Retrieval-Augmented Generation (RAG) and custom tools.  
Users can upload documents to create a knowledge base, chat with the assistant, and perform external actions via API integrations.  

## Repository Structure
-----
ai-assistant/
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── api.py               # FastAPI app principal
│   ├── embedding.py         # Funciones para chunking y embeddings
│   ├── tools.py             # Funciones para integración con APIs (Strapi, etc)
│   ├── db.py                # Funciones para conexión y queries a la DB
│   ├── requirements.txt     # Dependencias Python
│   └── README.md
│
├── database/
│   ├── data_ingestion.py    # Script para limpieza e ingreso de datos a la DB
│   └── README.md
│
├── cms/
│   ├── strapi_integration.py # Script o módulo para manejo de Strapi CMS
│   └── README.md
│
├── docs/
│   ├── architecture_diagram.png
│   ├── DEPLOY.md
│   └── planning.md
│
└── README.md
-----

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
