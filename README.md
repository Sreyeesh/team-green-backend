# Team Green — Barbershop Booking API

Django + Django REST Framework backend for the Team Green barbershop booking system.

---

## Requirements

- Python 3.10+
- pip

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Sreyeesh/team-green-backend.git
cd team-green-backend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and set a secure `SECRET_KEY`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Seed demo data

Populates a demo shop, 2 barbers, 4 services, and 3 bookings for tomorrow.

```bash
python manage.py seed
```

Demo credentials created by the seed:

| Field | Value |
|---|---|
| Admin email | `owner@freshcuts.com` |
| Admin password | `hackathon123` |
| Shop slug | `fresh-cuts` |

To wipe and re-seed from scratch:

```bash
python manage.py seed --flush
```

### 7. (Optional) Create a Django superuser

Required to access the Django admin panel at `/django-admin/`.

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

---

## API Documentation

Interactive Swagger UI is available at:

```
http://localhost:8000/api/docs/
```

OpenAPI schema (JSON) at:

```
http://localhost:8000/api/schema/
```

---

## API Reference

### Public Endpoints (no auth required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/shops/:slug/` | Shop details (name, description, logo, hours, address) |
| GET | `/api/shops/:slug/barbers/` | List barbers with photo, bio, specialties |
| GET | `/api/shops/:slug/services/` | Service menu (name, duration, price, category) |
| GET | `/api/shops/:slug/availability/` | Available time slots — query: `barber_id`, `service_id`, `date` |
| POST | `/api/bookings/` | Create a booking |
| GET | `/api/bookings/:id/` | Booking details by ID |
| GET | `/api/bookings/confirm/:code/` | Booking lookup by confirmation code |

#### Availability query example

```
GET /api/shops/fresh-cuts/availability/?barber_id=1&service_id=2&date=2026-04-01
```

#### Create booking body

```json
{
  "barber": 1,
  "service": 2,
  "datetime": "2026-04-01T10:00:00",
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com",
  "customer_phone": "+1 555 000 0001"
}
```

A successful booking returns a `confirmation_code` (e.g. `A3F9C1B2`) the customer can use to look up their booking later.

---

### Auth Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Shop owner signup — returns JWT |
| POST | `/api/auth/login/` | Returns JWT access + refresh tokens |
| POST | `/api/auth/token/refresh/` | Exchange refresh token for a new access token |

#### Register body

```json
{
  "email": "owner@myshop.com",
  "password": "securepassword",
  "shop_name": "My Barbershop"
}
```

#### Login body

```json
{
  "email": "owner@myshop.com",
  "password": "securepassword"
}
```

Both return:

```json
{
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>"
}
```

Include the access token in all admin requests:

```
Authorization: Bearer <access token>
```

---

### Admin Endpoints (JWT required)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/shop/` | Get your shop details |
| PUT | `/api/admin/shop/` | Update shop details |
| GET | `/api/admin/barbers/` | List barbers |
| POST | `/api/admin/barbers/` | Add a barber |
| PUT | `/api/admin/barbers/:id/` | Update a barber |
| DELETE | `/api/admin/barbers/:id/` | Remove a barber |
| GET | `/api/admin/services/` | List services |
| POST | `/api/admin/services/` | Add a service |
| PUT | `/api/admin/services/:id/` | Update a service |
| DELETE | `/api/admin/services/:id/` | Remove a service |
| GET | `/api/admin/bookings/` | List bookings — query: `date`, `status` |
| PUT | `/api/admin/bookings/:id/` | Update booking status (`pending`, `confirmed`, `cancelled`) |

---

## Data Models

```
Shop:    { id, slug, name, description, logo_url, address, phone, hours }
Barber:  { id, name, photo_url, bio, specialties[] }
Service: { id, name, description, duration_minutes, price, category }
Booking: { id, confirmation_code, shop, barber, service, datetime,
           duration_minutes, customer_name, customer_email,
           customer_phone, status, created_at }
```

`hours` format:
```json
{
  "mon": { "open": "09:00", "close": "18:00" },
  "tue": { "open": "09:00", "close": "18:00" },
  "sat": { "open": "10:00", "close": "17:00" },
  "sun": { "open": null, "close": null }
}
```

---

## Project Structure

```
team-green-backend/
├── accounts/        # Auth endpoints (register, login)
├── bookings/        # Booking model + public and admin booking endpoints
├── shops/           # Shop, Barber, Service models + all shop endpoints
│   └── management/
│       └── commands/
│           └── seed.py   # Demo data loader
├── core/            # Django project settings and root URLs
├── .env.example     # Environment variable template
├── manage.py
└── requirements.txt
```

---

## Frontend

The frontend lives at [Sreyeesh/team-green-frontend](https://github.com/Sreyeesh/team-green-frontend).
It proxies all `/api/*` requests to this backend on `localhost:8000` — no extra configuration needed during development.
