# ADR 0006: Linting and Code Formatting

## Context

It is important to maintain a consistent code style and automatically detect common errors.

## Decision

- `ruff` is used as the main linting and formatting tool.
- Formatting and linting rules are configured in `pyproject.toml`.
- `.editorconfig` is used for cross-platform formatting rules.
- A maximum line length of 88 characters is established.

## Consequences

- The code is more readable and consistent.
- Errors and bad practices are detected before reaching production.
- Collaboration between developers is facilitated.
