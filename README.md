# VerifyOnce – Full-stack Milestone 1

This package combines the selected GSAP-based frontend with a Flask API integration for the citizen registration, simulated OTP verification, login and protected profile flow.

## Stack
- Frontend: HTML, CSS, JavaScript; original adapted 8B Arcline GSAP landing page.
- Backend: Python + Flask + Flask-JWT-Extended.
- Current storage: temporary in-memory demo repository.
- Planned persistence: Supabase PostgreSQL, after the database teammate's schema is ready.

## Run on Windows / VS Code

1. Extract the ZIP and open the `VerifyOnce-FullStack-M1` folder in VS Code.
2. Open the terminal and run:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py run.py
```

3. Open `http://127.0.0.1:5000`.
4. Select **Create profile**, use fictional demo details, and submit.
5. The local backend responds with demo OTP `123456` (configurable in `backend/.env`). Enter it to complete the simulated verification.
6. You should reach the protected citizen dashboard. Sign out and try logging in with the same demo credentials.

The Flask server serves both the frontend and API on the same origin, so no separate frontend server or CORS configuration is required.

## API endpoints in this milestone

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend health |
| POST | `/api/auth/register` | Create pending demo account |
| POST | `/api/auth/otp/verify` | Simulated OTP verification; returns JWT |
| POST | `/api/auth/login` | Login verified demo account |
| GET | `/api/citizens/me` | Protected current citizen profile |
| GET | `/api/documents` | Protected empty placeholder |
| GET | `/api/applications` | Protected empty placeholder |

## Test

```powershell
cd backend
pytest -q
```

## Critical limitations

- The in-memory repository is for local integration testing only. All demo accounts disappear when the Flask server restarts.
- `123456` is a simulated demo OTP, not an SMS or a secure production OTP. Never deploy this demo configuration publicly.
- Citizen IDs generated here are demo-only identifiers after simulated contact verification. They are not official identity credentials and do not mean a government identity check occurred.
- No real Aadhaar/PAN or sensitive personal documents should be entered. Use fictional sample data only.
- Supabase/PostgreSQL is deliberately not wired yet because the database teammate owns the final schema. The repository adapter will be replaced once `schema.sql` and the integration notes are available.
- OCR, document uploads, scheme rules, officer review and application decisions are later milestones.
- The service-role key must only be used server-side and must never be placed in frontend JavaScript.

## Template credits
The adapted landing page retains the original template's licence and attribution. See `frontend/LICENSE` and `frontend/CREDITS.md`.
