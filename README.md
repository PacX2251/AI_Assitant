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
├── backend/
│   ├── chroma_db/
│   │   └── chroma.sqlite3
│   ├── my-strapi-app/
│   │   ├── .env
│   │   ├── .env.example
│   │   ├── .gitignore
│   │   ├── .strapi-updater.json
│   │   ├── favicon.png
│   │   ├── jsconfig.json
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   └── README.md
│   └── llm_api.py
├── database/
├── datasets/
│   ├── canciones_top.csv
│   ├── canciones_top_contexto.txt
│   ├── salud_2022.csv
│   ├── salud_2022_contexto.txt
│   ├── videojuegos_ventas.csv
│   └── videojuegos_ventas_contexto.txt
├── frontend/
│   ├── node_modules/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── .gitignore
│   ├── package-lock.json
│   ├── package.json
│   └── README.md
├── venv/
├── .git/
├── .gitignore
├── README.md
├── requirements.txt

```
- `frontend/`  
  React app for the chat interface and file uploads.

- `backend/`  
  FastAPI backend handling AI logic, embeddings, and API calls.
  Strapi Project

- `database/`  
  Scripts for data ingestion, cleaning, and storage in PostgreSQL.

## Getting Started

Please refer to `DEPLOY_LOCAL.md` for deployment instructions.

## Contact

For questions, contact [pacoroblesmoral@gmail.com]
