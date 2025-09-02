
# Infinite Technology - Real Estate CRM (Flask)
Modern, production-ready CRM for real estate teams. No external APIs.

## Setup (Local)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "from app import app; app.app_context().push(); from models import db; db.create_all()"
flask --app app run

## Deploy (Render)
- Build: pip install -r requirements.txt
- Start: gunicorn app:app
- ENV: SECRET_KEY, DATABASE_URL (from Render Postgres)
