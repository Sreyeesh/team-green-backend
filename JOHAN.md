# Backend Setup Guide for Johan

Hey Johan! This is everything you need to get the backend running locally and start hitting the API from the frontend.

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

Open `.env` and it should look like this — no changes needed for local dev:

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

The seed command gives you a ready-to-go demo shop:

| | |
|---|---|
| Shop slug | `fresh-cuts` |
| Admin email | `owner@freshcuts.com` |
| Admin password | `hackathon123` |
| Barbers | Marcus Reid, Priya Nair |
| Services | Classic Haircut, Skin Fade, Beard Trim, Cut & Beard Combo |
| Bookings | 3 pre-made bookings for tomorrow |

To wipe and start fresh: `python manage.py seed --flush`

---

## 4. Start the Server

> ⚠️ Port 8000 is taken on this machine by another app. Use **8080**.

```bash
python manage.py runserver 8080
```

---

## 5. API Docs (Swagger)

Once the server is running, open:

```
http://localhost:8080/api/docs/
```

Every endpoint is documented with request body, response shape, and a **Try it out** button — no Postman needed.

---

## 6. How the Frontend Connects

The frontend proxies all `/api/*` calls to `http://localhost:8080` automatically via Vite — no CORS setup needed, no hardcoded URLs.

Just make sure:
- Backend is running on port **8080**
- Frontend is running (`npm run dev`) — it'll be on `http://localhost:5173` or `5174`

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
POST /api/auth/register/    → { token, refresh, shop }
POST /api/auth/login/       → { token, refresh, shop }
POST /api/auth/token/refresh/
```

Store the `token` as `admin_token` in localStorage — the frontend already handles this.

### Admin (requires `Authorization: Bearer <token>` header)

```
GET  PUT  /api/admin/shop/
GET  POST /api/admin/barbers/
PUT  DELETE /api/admin/barbers/:id/
GET  POST /api/admin/services/
PUT  DELETE /api/admin/services/:id/
GET  /api/admin/bookings/?date=2026-04-01&status=pending
PUT  /api/admin/bookings/:id/
```

---

## 8. Troubleshooting

**`ModuleNotFoundError`** — make sure your venv is activated: `source venv/bin/activate`

**`Port already in use`** — use a different port: `python manage.py runserver 8081`

**`401 Unauthorized` on admin endpoints** — make sure you're sending the JWT: `Authorization: Bearer <token>`

**Empty responses** — run `python manage.py seed` to populate the database

**Need to reset everything** — `python manage.py seed --flush` then `python manage.py seed`
