# Local Deployment Guide for AI_Assistant

This guide helps you set up and run the AI_Assistant project locally, including database setup, backend, frontend, and Strapi CMS.

---

## 1. Clone the repository

```bash
git clone https://github.com/PacX2251/AI_Assitant.git
cd AI_Assitant
```
2. Install PostgreSQL and Setup Database
Make sure PostgreSQL is installed and running on your machine.

3. Automate Database Setup and Strapi .env Creation
We provide a script setup_db.sh that:

Creates PostgreSQL database and user (if they don't exist).

Generates .env file for Strapi with DB credentials.

Run it from the project root:

```bash
chmod +x setup_db.sh
./setup_db.sh
```
4. Run Strapi CMS Backend
```bash
cd backend/my-strapi-app
npm install
npm run develop
```
Strapi will run at: http://localhost:1337

5. Run Python Backend API
Open a new terminal:

```bash
cd AI_Assistant
source venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.llm_api:app --reload
```
Backend server runs at: http://localhost:8000

6. Run React Frontend
Open a new terminal:

```bash
cd frontend
npm install
npm start
```
Frontend available at: http://localhost:3000


## Notes
Keep all terminals open while running the services.

To stop any service, use Ctrl + C.

Make sure PostgreSQL service is running before starting Strapi.

## Contact
Questions? Contact: pacoroblesmoral@gmail.com