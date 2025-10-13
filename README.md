# The Greeters Ministry App (Flask + SQLite)

A minimal two-role app:

- **Admin**: create welcomers, create members, assign members to welcomers, set biweekly topics with Bible verses and activities
- **Welcomer**: log in and see a biweekly checklist of assigned members; check/uncheck items (auto-resets biweekly)

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
- Set Biweekly Topics with Bible verses and activities
- Delete welcomers and members
- View assignment status and checkoff progress

### Welcomer Dashboard:
- View biweekly topic, Bible verse, message, and activity
- Check off assigned members as contacted
- Automatic biweekly reset

## Biweekly Reset

The app uses a **biweekly period key** (e.g., `2025-B19`) and stores checkoffs per biweekly period. Each new biweekly period displays an unchecked list automatically—no manual reset needed.

## Notes

- Swap SQLite for Postgres by setting `DATABASE_URL` in `.env`.
- For production, set a strong `FLASK_SECRET_KEY`.
- If you want Firebase Auth/Firestore instead, the structure remains similar; swap data access in `models.py` with a Firestore service layer.
