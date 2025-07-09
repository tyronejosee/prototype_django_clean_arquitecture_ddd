# 🌐 Environment Variables

> [Disclaimer](../DISCLAIMER.md)

## Mandatory Variables

| Variable              | Description                         | Example                    |
|-----------------------|-----------------------------------|----------------------------|
| `DJANGO_SECRET_KEY`    | Secret key for Django              | `s3cr3t-k3y`               |
| `POSTGRES_DB`          | PostgreSQL database name           | `school_db`                |
| `POSTGRES_USER`        | Database user                     | `school_user`              |
| `POSTGRES_PASSWORD`    | Database password                 | `strongpassword`           |
| `POSTGRES_HOST`        | Database host                    | `db`                      |
| `POSTGRES_PORT`        | Database port                    | `5432`                    |
| `DJANGO_DEBUG`         | Django debug mode                 | `True` or `False`          |

## Optional Variables

| Variable              | Description                         | Example                    |
|-----------------------|-----------------------------------|----------------------------|
| `EMAIL_HOST`          | SMTP server for sending emails     | `smtp.gmail.com`           |
| `EMAIL_PORT`          | SMTP port                        | `587`                      |
| `EMAIL_HOST_USER`     | SMTP user                       | `user@gmail.com`           |
| `EMAIL_HOST_PASSWORD` | SMTP password                   | `password`                 |
| `REDIS_URL`           | URL to connect to Redis            | `redis://redis:6379/0`     |

## ⚠️ Recommendations

- Never upload `.env` to the repository
- Use a vault or secrets manager for production
- Document new variables when adding them
