<div align="center">
  <a href="https://github.com/tyronejosee/marketly" target="_blank">
    <img src="docs/logo.svg" alt="logo" width="80">
  </a>
</div>
<div align="center">
  <h1><strong>Marketly</strong></h1>
  <span>Ecommerce API</span>
</div>
<br>
<p align="center">
This repository implements a Django application following the principles of Clean Architecture and Domain-Driven Design (DDD). It serves as a practical example of how to structure a robust and maintainable application.
<p>
<p align="center">
  <a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="python-version">
  </a>
  <a href="https://www.djangoproject.com/">
  <img src="https://img.shields.io/badge/django-5.0.1-green" alt="django-version">
  </a>
  <a href="https://www.django-rest-framework.org/">
  <img src="https://img.shields.io/badge/drf-3.14.0-red" alt="django-rest-framework-version">
  </a>
</p>

## 📚 Documentation

- 🧭 Product
  - [Vision](./docs/product/vision.md)
  - [Roadmap](./docs/product/roadmap.md)
  - [Changelog](./docs/product/changelog.md)
  - [Team](./docs/product/team.md)
- ⚙️ Functional
  - [Functional Specifications](./docs/functional/functional-specs.md)
  - [Use Cases](./docs/functional/use-cases.md)
  - [Glossary](./docs/functional/glossary.md)
- 🏗️ Architecture/
  - [System Overview](./docs/architecture/system-overview.md)
  - [Components](./docs/architecture/components.md)
  - [Database Schema](./docs/architecture/database-schema.md)
  - [Security](./docs/architecture/security.md)
- 📘 Architecture Decision Records (ADR)
  - [0001 - Clean Architecture & DDD](./docs/architecture/adr/0001-clean-architecture-ddd.md)
  - [0002 - Framework](./docs/architecture/adr/0002-framework.md)
  - [0003 - Testing & Coverage](./docs/architecture/adr/0003-testing-coverage.md)
  - [0004 - Environment Configuration](./docs/architecture/adr/0004-enviroment-configuration.md)
  - [0005 - Docker](./docs/architecture/adr/0005-docker.md)
  - [0006 - Linting & Code Formatting](./docs/architecture/adr/0006-linting-code-formatting.md)
  - [0007 - Continuous Integration](./docs/architecture/adr/0007-continuous-integration.md)
  - [0008 - JWT-based Authentication](./docs/architecture/adr/0008-jwt-based-authentication.md)
  - [0009 - API Documentation](./docs/architecture/adr/0009-api-documentation.md)
  - [0010 - Branching Strategy](./docs/architecture/adr/0010-branching-strategy.md)
- 🚀 Operations
  - [Local Setup](./docs/operations/local-setup.md)
  - [Deployment](./docs/operations/deployment.md)
  - [DevOps Guide](./docs/operations/devops-guide.md)
  - [Environment Variables](./docs/operations/environment-variables.md)
  - [Monitoring](./docs/operations/monitoring.md)
- 🧪 Testing
  - [Test Strategy](./docs/testing/test-strategy.md)
  - [Coverage](./docs/testing/coverage.md)
- 🤝 Contributing
  - [Contributing Guide](./docs/contributing/contributing.md)
  - [Commit Convention](./docs/contributing/commit-convention.md)
  - [Code Style](./docs/contributing/code-style.md)

## ⚙️ Installation

Clone the repository.

```bash
git clone git@github.com:tyronejosee/project_marketly.git
cd project_marketly
```

>💡 We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) for this project. It is a fast, modern Python package manager that handles dependency resolution, virtual environments, and installs with superior performance and safety.

Create a virtual environment.

```bash
uv venv
```

Install the project dependencies.

```bash
uv pip install .
```

Activate the virtual environment.

```bash
.venv\Scripts\activate
```

Create a copy of the `.env.example` file and rename it to `.env`.

```bash
cp .env.example .env
```

**Update the values of the environment variables (Important).**

> 💡 Make sure to correctly configure your variables before building the container.

## 🐳 Docker

Build your container; it will take time the first time, as Docker needs to download all dependencies and build the image.
Use the `-d` (detached mode) flag to start your containers in the background.
Use the `--build` flag if you have changes and need to rebuild.

```bash
docker compose up
docker compose up -d
docker compose up --build
```

Stop the running containers (does not remove them).

```bash
docker compose stop
```

Start previously created and stopped containers.

```bash
docker compose start
```

Show container logs in real-time.

```bash
docker compose logs -f
```

Restart a service with issues (Replace `<service_name>`).

```bash
docker compose restart <service_name>
```

Remove your container.

```bash
docker compose down
```

## 🐍 Django

Access the `web` service console that runs Django.

```bash
docker compose exec web bash
```

Inside the Django console, create the migrations.

```bash
python manage.py makemigrations
```

Run the migrations.

```bash
python manage.py migrate
```

If you need to be more specific, use:

```bash
python manage.py migrate <app_label> <migration_name>
```

List all available migrations and their status.

```bash
python manage.py showmigrations
```

> 💡 Manually create the migration if Django skips an app; this happens because Django did not find the `/migrations` folder.

Create a superuser to access the entire site without restrictions.

```bash
python manage.py createsuperuser
```

Log in to `admin`:

```bash
http://127.0.0.1:8000/admin/
```

Access Swagger or Redoc.

```bash
http://127.0.0.1:8000/api/schema/swagger/
http://127.0.0.1:8000/api/schema/redoc/
```

## 🚨 Important Notes

Check the creation of migrations before creating them.

```bash
docker compose exec web python manage.py makemigrations users
```

> 💡 Checking migrations before their creation is necessary to avoid inconsistencies in user models.

## 🐘 PostgreSQL

Access the PostgreSQL console.

```bash
docker compose exec db psql -U postgres -d fandomhub_db
```

List all the tables in the database.

```bash
\dt
```

Show the detailed structure of a specific table.

```bash
\d <table_name>
```

Create a backup of your database (Optional).

```bash
docker compose exec web python manage.py dumpdata > backup.json
```

Load the created backup if needed (Optional).

```bash
docker compose exec web python manage.py loaddata
```

## 🧪 Testing

Run all tests.

```bash
pytest
```

Run tests for type and domain.

```bash
pytest tests/<type>/<domain>
```

Run unit tests for a specific domain (with coverage).

```bash
pytest tests/unit/<domain> -o addopts="--cov=src/modules/<domain> --cov-report=term-missing"
```

## ⚖️ License

This project is under the [MIT License](https://github.com/tyronejosee/project_marketly/blob/main/LICENSE).

Enjoy! 🎉
