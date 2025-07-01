# ADR 0002: Django as the Main Framework

## Context

A robust framework is required to accelerate development, leverage the Python ecosystem, and facilitate integration with relational databases.

## Decision

- Django is used as the main framework.
- Django REST Framework is used for the presentation layer (API).
- A custom user model (`UserModel`) is configured.
- PostgreSQL is used as the default database.

## Consequences

- Django's administration and authentication tools are leveraged.
- Integration with other services and libraries in the Django ecosystem is facilitated.
- The domain remains independent of Django, but the infrastructure implements it using Django components.
