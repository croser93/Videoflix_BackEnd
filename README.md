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

Django itself runs locally in a virtual environment. PostgreSQL, Redis and MailHog run as Docker containers alongside it.

1. Clone repository
```bash
git clone https://github.com/croser93/Videoflix_BackEnd.git
```

2. Go to project
```bash
cd Videoflix_BackEnd
```

3. Create virtual environment
```bash
python -m venv .venv
```

4. Activate virtual environment — Linux/Mac
```bash
source .venv/bin/activate
```

4. Activate virtual environment — Windows
```bash
.venv\Scripts\activate
```

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Create your `.env` file from the template
```bash
cp .env.template .env
```
Then fill in the values — see [Environment Variables](#environment-variables) below for what's needed. Since Django runs outside Docker, `DB_HOST` and `REDIS_HOST` should be set to `localhost`.

7. Start the infrastructure containers (Postgres, Redis, MailHog)
```bash
docker-compose up -d db redis mailhog
```

8. Create migration files
```bash
python manage.py makemigrations
```

9. Run database migrations
```bash
python manage.py migrate
```

10. Create a superuser (optional, for Django Admin access)
```bash
python manage.py createsuperuser
```

11. Start the development server
```bash
python manage.py runserver
```

The API is now available at `http://localhost:8000/api/`.

### Background worker (Redis Queue)

Video conversion (HLS transcoding via ffmpeg) and email sending run as asynchronous jobs and require an RQ worker to process the queue. Without a running worker, uploaded videos will never be transcoded and activation/reset emails will stay queued but never sent.

Linux/Mac:
```bash
python manage.py rqworker default
```

Windows — `os.fork()` is not available on Windows, so the `SimpleWorker` class must be used instead:
```bash
python manage.py rqworker default --worker-class rq.worker.SimpleWorker
```

### Testing emails with MailHog

By default (`EMAIL_HOST=mailhog`), all outgoing emails (account activation, password reset) are caught by MailHog instead of being sent to a real inbox. Once the containers are running, open MailHog's web UI at:

```
http://localhost:8025
```

Every email triggered by the API (e.g. after registering a new user or requesting a password reset) will appear there instead of being delivered to a real mailbox — useful for testing the full flow without a real SMTP provider.

## Environment Variables

The `.env` file (copied from `.env.template` in step 3 above) needs the following variables:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True`/`False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts, e.g. `localhost,127.0.0.1` |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` | PostgreSQL credentials |
| `DB_HOST` / `DB_PORT` | PostgreSQL host/port — `localhost`/`5432` when Django runs outside Docker |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` | Redis connection used by django-rq — `localhost` when Django runs outside Docker |
| `REDIS_LOCATION` | Redis URL used by the cache backend, e.g. `redis://redis:6379/1` |
| `EMAIL_HOST` / `EMAIL_PORT` | SMTP host/port (`mailhog`/`1025` for local testing) |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | SMTP credentials (leave empty for MailHog) |
| `EMAIL_USE_TLS` | `True`/`False` |
| `DEFAULT_FROM_EMAIL` | Sender address used for outgoing emails |

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
