# Backend Setup Guide for Johan

Hey Johan! This is everything you need to get the backend running locally, hit the API from the frontend, and demo it during the presentation.

---

## Presentation Checklist

Before going on stage, make sure:

- [ ] Backend running: `python manage.py runserver 8080`
- [ ] Frontend running: `npm run dev`
- [ ] Seed data loaded: `python manage.py seed`
- [ ] Swagger open in a tab: `http://localhost:8080/api/docs/`
- [ ] Frontend open in a tab: `http://localhost:5174/`
- [ ] Admin login ready (see credentials below)

---

## Demo Login Credentials

Use these to log into the admin panel during the presentation:

| Field    | Value                    |
|----------|--------------------------|
| Email    | `owner@freshcuts.com`    |
| Password | `hackathon123`           |

**Via the frontend** — go to `http://localhost:5174/` and log in with the credentials above.

**Via Swagger** — go to `http://localhost:8080/api/docs/`, find **LoginView**, click **Try it out**, and enter:
```json
{
  "email": "owner@freshcuts.com",
  "password": "hackathon123"
}
```

**Via terminal** — quick test:
```bash
curl -s -X POST http://localhost:8080/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "owner@freshcuts.com", "password": "hackathon123"}'
```

The response gives you a `token` — use it in admin requests:
```
Authorization: Bearer <token>
```

---

## Demo Shop Data

The seed command pre-loads everything needed for the demo:

| | |
|---|---|
| Shop name | Fresh Cuts Barbershop |
| Shop slug | `fresh-cuts` |
| Barbers | Marcus Reid, Priya Nair |
| Services | Classic Haircut · Skin Fade · Beard Trim & Shape · Cut & Beard Combo |
| Bookings | 3 pre-made bookings for tomorrow (confirmed + pending) |

To reset demo data at any point: `python manage.py seed --flush && python manage.py seed`

---

## 1. Clone & Setup

```bash
git clone https://github.com/Sreyeesh/team-green-backend.git
cd team-green-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Environment Variables

```bash
cp .env.example .env
```

Open `.env` — no changes needed for local dev:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

---

## 3. Database & Seed Data

```bash
python manage.py migrate
python manage.py seed
```

---

## 4. Start the Server

> ⚠️ Port 8000 is taken on this machine by another app. Use **8080**.

```bash
python manage.py runserver 8080
```

---

## 5. API Docs (Swagger)

```
http://localhost:8080/api/docs/
```

Every endpoint has request body, response shape, and a **Try it out** button — no Postman needed.

---

## 6. How the Frontend Connects

The frontend proxies all `/api/*` calls to `http://localhost:8080` automatically via Vite — no CORS setup, no hardcoded URLs.

Make sure:
- Backend is on port **8080**
- Frontend is running (`npm run dev`) — available at `http://localhost:5173` or `5174`

---

## 7. Quick API Reference

### Public (no auth needed)

```
GET  /api/shops/fresh-cuts/
GET  /api/shops/fresh-cuts/barbers/
GET  /api/shops/fresh-cuts/services/
GET  /api/shops/fresh-cuts/availability/?barber_id=1&service_id=1&date=2026-04-01
POST /api/bookings/
GET  /api/bookings/:id/
GET  /api/bookings/confirm/:code/
```

### Auth

```
POST /api/auth/register/         → { token, refresh, shop }
POST /api/auth/login/            → { token, refresh, shop }
POST /api/auth/token/refresh/
```

### Admin (requires `Authorization: Bearer <token>`)

```
GET  PUT    /api/admin/shop/
GET  POST   /api/admin/barbers/
PUT  DELETE /api/admin/barbers/:id/
GET  POST   /api/admin/services/
PUT  DELETE /api/admin/services/:id/
GET         /api/admin/bookings/?date=2026-04-01&status=pending
PUT         /api/admin/bookings/:id/
```

---

## 8. Troubleshooting

**`ModuleNotFoundError`** — activate the venv: `source venv/bin/activate`

**`Port already in use`** — try: `python manage.py runserver 8081`

**`401 Unauthorized`** — include the JWT header: `Authorization: Bearer <token>`

**Empty API responses** — seed the database: `python manage.py seed`

**Need to reset everything** — `python manage.py seed --flush` then `python manage.py seed`
