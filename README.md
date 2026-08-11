[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&labelColor=092E20)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-red?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens)](https://jwt.io/)

# Videoflix Backend
Backend API for a Netflix-clone streaming platform.
Learning project as part of the Developer Akademie.

## About the Project
Videoflix is the backend for a Netflix-style streaming platform. It handles user registration and authentication (including email activation and password reset), stores video metadata, and automatically transcodes uploaded videos into multiple HLS resolutions (480p/720p/1080p) for adaptive streaming. Video conversion and email delivery run asynchronously in the background via Redis Queue, so uploads and registrations don't block the API.

## Tech Stack

| Technology | Version |
|------------|---------|
| Python | 3.14.4 |
| Django | 6.0.7 |
| Django REST Framework | 3.17.1 |
| djangorestframework-simplejwt | 5.5.1 |
| django-cors-headers | 4.9.0 |
| django-redis | 7.0.0 |
| django-rq | 4.1.1 |
| Pillow | 12.3.0 |
| psycopg2-binary | 2.9.12 |
| whitenoise | 6.12.0 |
| Database | PostgreSQL |
| Authentication | JWT (HttpOnly cookies) |

## Installation & Setup

The entire project runs via Docker Compose — PostgreSQL, Redis, MailHog and the Django app itself all run as containers. No local Python installation is required.

1. Clone repository
```bash
git clone https://github.com/croser93/Videoflix_BackEnd.git
```

2. Go to project
```bash
cd Videoflix_BackEnd
```

3. Create your `.env` file from the template
```bash
cp .env.template .env
```

### Environment Variables

Before starting the containers, open `.env` and go through the following points one by one.

#### 1. `SECRET_KEY`
The template ships with a placeholder value — replace it with a real generated key. Generate one with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the printed value into `.env`, for example:
```
SECRET_KEY=django-insecure-8f$k2m...
```

#### 2. Database credentials
These three values are used both by Django and to initialize the Postgres container itself, so pick real values here (they don't need to match anything else, you're defining them for the first time).

| Variable | What it is |
|----------|-------------|
| `DB_NAME` | Name of the database that gets created |
| `DB_USER` | Username Django uses to connect to it |
| `DB_PASSWORD` | Password for that user |

Example:
```
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=a-strong-password-here
```

#### 3. `ALLOWED_HOSTS`
Comma-separated list of hostnames the Django server is allowed to respond to. For local development this is usually enough as-is:
```
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 4. `CSRF_TRUSTED_ORIGINS`
Comma-separated list of frontend origin(s) that are allowed to send requests to the API. This must match wherever your frontend actually runs — if it doesn't, requests from the frontend will be rejected. Example, if your frontend runs on port 4000:
```
CSRF_TRUSTED_ORIGINS=http://localhost:4000,http://127.0.0.1:4000
```

#### 5. `DB_HOST` / `DB_PORT`
Leave these as they are in the template (`db` / `5432`) — that's the internal Docker network name of the Postgres container, not something you need to change.

#### 6. Email settings
By default, `.env.template` routes all emails (account activation, password reset) to the MailHog container instead of a real inbox — see [Testing emails with MailHog](#testing-emails-with-mailhog) below. This requires no changes and is the easiest way to test the project. If you want real emails to actually be delivered, replace these with real SMTP credentials instead (e.g. a Gmail address with an App Password):
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your.address@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your.address@gmail.com
```

#### 7. `DJANGO_SUPERUSER_EMAIL` / `DJANGO_SUPERUSER_PASSWORD`
On first startup, the container automatically creates a Django Admin superuser from these two values — no separate `createsuperuser` command needed. Only email and password are required (there's no username field). Example:
```
DJANGO_SUPERUSER_EMAIL=admin@videoflixcom
DJANGO_SUPERUSER_PASSWORD=choose-a-password
```
### Start Docker 
Build and start all containers (Postgres, Redis, MailHog, Web)
```bash
docker-compose up --build
```

That's it — on startup, the web container automatically waits for PostgreSQL, runs `makemigrations`/`migrate`, creates a superuser from your `.env` credentials, starts the Redis Queue worker, and launches the server. No manual migration or `createsuperuser` step is needed.

The API is now available at `http://localhost:8000/api/`.

### Testing emails with MailHog

By default, the `.env.template` points `EMAIL_HOST` at the `mailhog` container instead of a real SMTP provider. As long as that's the case, every outgoing email (account activation, password reset) is caught by MailHog instead of being delivered to a real inbox. Once the containers are running, open MailHog's web UI at:

```
http://localhost:8025
```

Every email triggered by the API (e.g. after registering a new user or requesting a password reset) will appear there — useful for testing the full flow without a real SMTP provider. See the warning above for switching to real email delivery.

## Project Structure

```
Videoflix_BackEnd/
├── core/               # Project configuration (settings, urls, wsgi)
├── auth_app/           # Custom user model, registration, login, activation, password reset (JWT via HttpOnly cookies)
├── media_app/          # Video model, HLS transcoding tasks/signals, video listing and streaming endpoints
└── docker-compose.yml  # Postgres, Redis, MailHog and web service definitions
```

---
Learning project as part of the Developer Akademie.
