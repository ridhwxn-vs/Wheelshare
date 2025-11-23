# Wheelshare

**Wheelshare** is a lightweight, temporary bicycle/scooter renting web application built for college campuses. It uses a Django backend with HTML templates for the web UI.
The project was previously hosted on Railway with a PostgreSQL database.

> **Temporary cycle-renting web app for college campuses — Django backend, HTML frontend, previously hosted on Railway with PostgreSQL.**

---

## 🚲 Key Features

* Browse available cycles by station/location
* Reserve and release cycles for short campus rides
* Simple admin interface (Django admin) to manage inventory and stations
* Designed for short-term campus deployments (events, pilots)

---

## 🛠️ Tech Stack

* **Backend:** Python + Django
* **Frontend:** HTML templates (Django templating)
* **Database:** PostgreSQL (used during Railway deployment)
* **Recommended Python:** 3.10+

---

## ⚙️ Getting Started (Local Development)

These instructions assume a standard Django project structure (`manage.py` at project root).
Replace filenames/paths if your project differs.

---

### 1. Clone the repository

```bash
git clone https://github.com/ridhwxn-vs/Wheelshare.git
cd Wheelshare
```

---

### 2. Create and activate a Python virtual environment

```bash
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

If not, install Django and helpers manually:

```bash
pip install django psycopg2-binary python-dotenv dj-database-url
```

---

### 4. Environment variables

Create a `.env` file (or export variables) with at least:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@host:port/dbname
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

* If using `dj-database-url`, `DATABASE_URL` will be parsed automatically.
* For local SQLite, update settings or set `DATABASE_URL=sqlite:///db.sqlite3`.

---

### 5. Database setup & migrations

```bash
python manage.py migrate
```

(Optional) Create an admin user:

```bash
python manage.py createsuperuser
```

---

### 6. Run the development server

```bash
python manage.py runserver
```

Visit: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📁 Expected Project Structure

* `manage.py`
* `<project_package>/settings.py`
* `<app>/models.py`, `views.py`, `templates/`, `static/`
* `requirements.txt`
* `README.md`

---

## 🚀 Railway / Production Notes

* Set `DATABASE_URL` in Railway environment variables.
* Set `SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`.
* Use a `Procfile` if required:

```
web: gunicorn <project_package>.wsgi --log-file -
```

* Serve static files using WhiteNoise or similar.
* Run collectstatic during deployments:

```bash
python manage.py collectstatic --noinput
```

* Use `dj-database-url` for database parsing in `settings.py`.

---

## 🔧 Recommended Improvements / TODO

* Add fixture/seed script for local sample stations & bikes.
* Add tests + CI workflow (GitHub Actions).
* Add Dockerfile + docker-compose for easier dev environment setup.

---

## 🔐 Security Notes

* Never commit `SECRET_KEY` or production `DATABASE_URL`.
* Always set `DEBUG=False` in production.
* Configure allowed hosts & secure TLS.

---

## 🐳 Sample Dockerfile (Optional)

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

---

## 👤 Maintainer / Contact

* **Repository Owner:** ridhwxn-vs

---
