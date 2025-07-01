# ADR 0005: Project Dockerization

## Context

The goal is to facilitate deployment, portability, and consistency of the development and production environments.

## Decision

- Docker is used to containerize the application and its dependencies.
- A `Dockerfile` is defined for the Django application image.
- `docker-compose` is used to orchestrate services such as the database and the web application.
- Environment variables are managed through `.env` files.

## Consequences

- The environment is reproducible and easy to set up on any machine.
- Deployment on servers and cloud services is simplified.
- New developers can quickly start the local environment.
