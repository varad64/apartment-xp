# Apartment Society – Frontend

A small React (Vite) UI for the FastAPI backend in the parent folder.

It shows the flat list and total chargeable area, and lets you submit the
security, electricity and water bills (as an amount or a JPEG for OCR) to see
each flat's share.

## Run

1. Start the backend from the project root:

   ```bash
   uvicorn main:app --reload
   ```

2. In another terminal, start the frontend from this folder:

   ```bash
   npm install
   npm run dev
   ```

3. Open http://localhost:5173.

The backend URL defaults to `http://localhost:8000`. To change it, create
`frontend/.env.local`:

```bash
VITE_API_URL=http://localhost:8000
```
