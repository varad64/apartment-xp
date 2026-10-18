# Apartment Society

A FastAPI backend for splitting society bills across flats, with a minimal React frontend.
The project uses Google Deepmind's open weight model - gemma3:4b for OCR capabilities. These are required to parse images of utility bills to extract the amount directly.

The application backend is <b>deployed to render</b> & the frontend is accessible at `https://varad64.github.io/apartment-xp/`

<img width="1498" height="1000" alt="image" src="https://github.com/user-attachments/assets/da9ae1a7-faac-4957-9762-002eca24a14a" />

<img width="1314" height="736" alt="image" src="https://github.com/user-attachments/assets/3ce4d172-76ff-48a8-a8a9-24e4a02810ca" />

<img width="1270" height="982" alt="image" src="https://github.com/user-attachments/assets/4d726a5b-ddde-4d09-923d-1878ce6c4d7f" />

The gemma model is running locally and is being provided to the backend as a service via a cloudflare tunnel.
