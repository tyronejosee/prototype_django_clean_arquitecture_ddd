# ADR 0008: JWT-based Authentication

## Context

A secure and scalable authentication is required for the API, especially if it is exposed to mobile clients or modern frontends.

## Decision

- JWT-based authentication will be used for the API.
- Libraries such as `djangorestframework-simplejwt` will be evaluated for implementation.
- Protected endpoints will require a valid token to access.

## Consequences

- Integration with SPA and mobile applications is facilitated.
- The authentication system is more scalable and decoupled from traditional Django sessions.
- The token lifecycle and its secure storage on the client must be managed.
