# ⚙️ Local Setup

> [Disclaimer](../DISCLAIMER.md)

## 📝 Requirements

- Docker & Docker Compose installed
- Git installed
- Python 3.11+ (optional for local testing outside container)

## 📥 Clone repository

```bash
git clone prototype_django_clean_arquitecture_ddd
cd prototype_django_clean_arquitecture_ddd
````

## 🔧 Environment variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` as needed (databases, keys, etc.)

## 🚀 Start services

```bash
docker compose up --build
```

This will start:

- Django API + DRF
- PostgreSQL
- Adminer for DB management (pending)

## 🛠️ Run migrations

Inside the web container:

```bash
docker compose exec web python manage.py migrate
```

## ✅ Run tests

```bash
docker compose exec web pytest
```

## 🔗 Access

- API: [http://localhost:8000/api/](http://localhost:8000/api/)
- Adminer: [http://localhost:8080/](http://localhost:8080/)
