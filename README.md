# Apartment Society

A FastAPI backend for splitting society bills across flats, with a minimal React frontend.
The project uses Google Deepmind's open weight model - gemma3:4b for OCR capabilities. These are required to parse images of utility bills to extract the amount directly.

The application backend is <b>deployed to render</b> & the frontend is accessible at `https://varad64.github.io/apartment-xp/`

The gemma model is running locally and is being provided to the backend as a service via a cloudflare tunnel.
