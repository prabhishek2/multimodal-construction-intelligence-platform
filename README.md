# Multimodal Construction Intelligence Platform

A Skill Wallet capstone starter for construction planning and site decision support, built with React + Vite and FastAPI.

## Modules
- Site safety/PPE checklist (manual-review demo; no computer-vision model connected yet)
- Crack observation workflow (not a structural diagnosis)
- Indicative construction budget and valuation in INR
- Weather-aware site advisory and rule-based site assistant
- FastAPI JSON endpoints and OpenAPI docs

## Stack
React 18, Vite, Python, FastAPI, Pydantic, pytest.

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
API docs: http://localhost:8000/docs

### Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. Set `VITE_API_URL` to your deployed API URL when hosting the frontend.

## API
`GET /api/health`, `GET /api/features`, `POST /api/safety`, `POST /api/cracks`, `POST /api/valuation`, `POST /api/advisory`, `POST /api/chat`.

## Deployment
Backend: deploy `backend` as a Render web service with build `pip install -r requirements.txt` and start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Frontend: import this repo into Vercel, set root directory to `frontend`, framework Vite, and environment variable `VITE_API_URL` to the backend URL. Add the exact frontend origin to CORS in `backend/main.py` before production.

## Important limitations
This is an initial runnable demo, not a complete multimodal AI system. Image endpoints return transparent manual-review placeholders and do not claim to detect PPE or classify cracks from pixels. Budget rates and material quantities are illustrative only. Do not use this app as a substitute for qualified safety or structural engineering review.

## Tests
```bash
cd backend
pytest -q
```
