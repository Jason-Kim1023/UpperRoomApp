# The Upper Room App (Flask + SQLite)

A minimal two-role app:

- **Admin**: create welcomers, create members, assign members to welcomers, set weekly topics with Bible verses and activities
- **Welcomer**: log in and see a weekly checklist of assigned members; check/uncheck items (auto-resets weekly)

## Quick Start

```bash
cd welcome-app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# (optional) cp .env.example .env and edit secrets
python app.py
```

Open: http://127.0.0.1:5000

## Features

### Admin Dashboard:
- Create Welcomers (email + temp password)
- Create Members
- Assign Member → Welcomer (multiple selection)
- Set Weekly Topics with Bible verses and activities
- Delete welcomers and members
- View assignment status and checkoff progress

### Welcomer Dashboard:
- View weekly topic, Bible verse, message, and activity
- Check off assigned members as contacted
- Automatic weekly reset

## Weekly Reset

The app uses an **ISO week key** (e.g., `2025-W38`) and stores checkoffs per week. Each new week displays an unchecked list automatically—no manual reset needed.

## Notes

- Swap SQLite for Postgres by setting `DATABASE_URL` in `.env`.
- For production, set a strong `FLASK_SECRET_KEY`.
- If you want Firebase Auth/Firestore instead, the structure remains similar; swap data access in `models.py` with a Firestore service layer.
