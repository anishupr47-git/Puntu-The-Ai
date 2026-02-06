# PUNTU (local-first AI companion)

PUNTU is a premium, local-first AI companion with a liquid UI/UX. It runs fully offline with Ollama, a local Postgres database, and a React + FastAPI stack. No paid services, no keys.

## Stack
- Frontend: React + Vite + Tailwind + Framer Motion
- Backend: FastAPI + SQLAlchemy + Postgres
- Local LLM: Ollama (http://localhost:11434)
- Memory: sentence-transformers (all-MiniLM-L6-v2) stored in Postgres

## Requirements
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Ollama installed locally

## Setup
1. Install Ollama and pull a model:
   - `ollama pull llama3`
2. Create a Postgres database and user (local or hosted). Neon works fine; use the connection string with `sslmode=require`.
3. Backend env:
   - Copy `backend/.env.example` to `backend/.env` and edit values.
4. Frontend env:
   - Copy `frontend/.env.example` to `frontend/.env` and edit values.
5. Install backend deps:
   - `pip install -r backend/requirements.txt`
6. Initialize database:
   - From `backend`: `python -m app.init_db` or `backend/scripts/init_db.ps1`
7. Seed datasets (songs, movies, clubs, national teams, football matches):
   - From `backend`: `python -m app.seed_db` or `backend/scripts/seed_db.ps1`
   - To reseed after updates: `set SEED_FORCE=1` (Windows) or `SEED_FORCE=1` (bash), then run again
8. Run backend:
   - `backend/scripts/dev.ps1`
9. Install frontend deps:
   - From `frontend`: `npm install`
10. Run frontend:
   - `npm run dev`

## Demo Steps
1. Open `http://localhost:5173`.
2. Click the floating PUNTU orb to open the panel.
3. Use Ask/Decide/Plan/Create modes for streaming responses and structured guidance.
4. Explore Songs, Movies, and Football modules for local recommendations and predictions.

## Notes
- The embedding model downloads on first use.
- Ollama streaming is proxied through the backend.
- No Docker is required.
