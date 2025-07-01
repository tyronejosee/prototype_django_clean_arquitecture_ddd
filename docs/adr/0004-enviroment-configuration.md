# ADR 0004: Environment Configuration

## Context

The project must be easily configurable for different environments (development, production, CI/CD).

## Decision

- `python-decouple` is used to manage environment variables.
- A `.env.example` file is provided as a template.
- Database configuration and secret keys are extracted from the environment.

## Consequences

- It is easy to change the configuration without modifying the source code.
- Security is improved by not exposing secrets in the repository.
