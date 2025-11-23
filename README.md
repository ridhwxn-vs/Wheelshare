```markdown
# Wheelshare

Wheelshare is a lightweight, temporary bicycle/scooter renting web application built for college campuses. It uses a Django backend with HTML templates for the web UI. The project was previously hosted on Railway with a PostgreSQL database.

> Temporary cycle-renting web app for college campuses — Django backend, HTML frontend, previously hosted on Railway with PostgreSQL.

Key features
- Browse available cycles by station/location
- Reserve and release cycles for short campus rides
- Simple admin interface (Django admin) to manage inventory and stations
- Designed for short-term campus deployments (events, pilots)

Tech stack
- Backend: Python + Django
- Frontend: HTML templates (Django templating)
- Database: PostgreSQL (used during Railway deployment)
- Recommended Python: 3.10+

Getting started (local development)
These instructions assume this repo follows a standard Django structure (manage.py at project root). Replace filenames/paths if your project uses different names.

1. Clone the repository
```bash
git clone https://github.com/ridhwxn-vs/Wheelshare.git
cd Wheelshare
```

2. Create and activate a Python virtual environment
```bash
python3 -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install dependencies
- If a requirements.txt exists:
```bash
pip install -r requirements.txt
```
- If not, install Django and helpers:
```bash
pip install django psycopg2-binary python-dotenv dj-database-url
```

4. Environment variables
Create a .env file (or set environment variables) with at least:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@host:port/dbname  # used for production/postgres
# Optional / local:
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```
If using dj-database-url in settings, DATABASE_URL will be parsed automatically. For local SQLite development, update settings to use sqlite3 or set DATABASE_URL accordingly (sqlite:///db.sqlite3).

5. Database setup and migrations
```bash
python manage.py migrate
# (optional) create a superuser for Django admin
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000 in your browser.

Project structure (expected)
- manage.py
- <project_package>/settings.py
- <app>/models.py, views.py, templates/, static/
- requirements.txt
- README.md

Railway / production notes
- The project was previously hosted on Railway using PostgreSQL. Typical setup steps:
  - Set DATABASE_URL in Railway environment variables to the Railway Postgres URL.
  - Set SECRET_KEY and DJANGO_ALLOWED_HOSTS appropriately.
  - Use a Procfile or Docker container for deployment if Railway expects it. Example Procfile:
    ```
    web: gunicorn <project_package>.wsgi --log-file -
    ```
  - Use whitenoise or proper static file hosting; run collectstatic in deploy steps:
    ```
    python manage.py collectstatic --noinput
    ```
- For database URL parsing, include dj-database-url and update settings.py to use dj_database_url.config() for DATABASES['default'].

Recommended improvements / TODOs
- Add a seed/fixture script to populate stations and bikes for local testing.
- Add simple tests and a CI workflow (GitHub Actions) that runs migrations and tests.
- Add Dockerfile and docker-compose for local reproducible dev environment.

Security notes
- Do not commit SECRET_KEY or production DATABASE_URL to the repo.
- Ensure DEBUG=False in production and configure allowed hosts and secure TLS.

Sample Dockerfile (optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "<project_package>.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Maintainer / Contact
- Repository owner: ridhwxn-vs
