# Apartment Society

A FastAPI backend for splitting society bills across flats, with a small React frontend.

## Backend

```bash
uv sync
uvicorn main:app --reload
```

API runs at http://localhost:8000. Bill image OCR needs Ollama running locally with `gemma3:4b`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173/apartment-app/ (the app uses this base path).
