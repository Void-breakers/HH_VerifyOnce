# VerifyOnce frontend – GSAP landing page + citizen portal prototype

This package adapts the selected 8B Arcline GSAP template for VerifyOnce and adds initial citizen-facing screens.

## Included
- `index.html` – animated VerifyOnce landing page adapted from the 8B Arcline GSAP template.
- `login.html` – citizen sign-in screen (local demo only).
- `register.html` – citizen registration screen (local demo only).
- `dashboard.html` – sample citizen dashboard with profile, documents, applications and services sections.
- `app.css`, `app.js` – shared styling and demo-only interactions.
- `LICENSE`, `CREDITS.md` – original template licence and attribution.

## Run locally
From this folder, run:
```powershell
py -m http.server 5500
```
Open `http://127.0.0.1:5500`.

The landing page uses GSAP, ScrollTrigger and Lenis from a CDN; internet access is needed for those animations. The other screens use local CSS/JS.

## Demo flow
1. Open the landing page and select **Create profile**.
2. Enter fictional details on the registration page.
3. The browser opens the sample citizen dashboard.
4. You can also sign in using any valid-looking email/mobile and a password of at least six characters.

## Important: prototype, not production authentication
Forms do not call a backend. Demo details are held in browser `sessionStorage` only. No OTP is sent, no identity is verified, and no Citizen ID is generated. Do not enter real personal documents or sensitive information. Replace the demo handlers with Flask API calls before using real accounts.

## Planned backend integration
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/otp/request` and `/api/auth/otp/verify` (simulated OTP for hackathon)
- `GET /api/citizens/me`
- `GET /api/applications`
- `GET /api/documents`

The Supabase service-role key must remain server-side. Use fictional sample documents for the hackathon demo. OCR extraction is not proof of document authenticity.

## Attribution
The adapted landing page retains the original 8B Arcline template's MIT-licensed code. See `LICENSE` and `CREDITS.md` for source, asset and font details.
