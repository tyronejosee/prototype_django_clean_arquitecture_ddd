# ADR 0009: API Documentation

## Context

It is essential that API consumers (frontend, mobile apps, integrators) have access to clear and up-to-date documentation.

## Decision

- An automatic documentation tool will be used, such as Swagger or Redoc using drf-spectacular.
- Documentation will be generated from DRF serializers and views.
- An endpoint `/docs` or `/swagger` will be exposed and accessible in development.

## Consequences

- Developers can easily consult and test the API.
- Friction in integration with other teams or services is reduced.
- Documentation remains synchronized with the code.
