# ADR 0003: Testing and Coverage

## Context

Ensuring software quality through automated testing and code coverage measurement is essential.

## Decision

* `pytest` and `pytest-django` are used for testing.
* Test code is organized into `unit`, `integration`, and `e2e` folders.
* `coverage` and `django-coverage-plugin` are used to measure code coverage.
* Migration files and test files are excluded from coverage reports.

## Consequences

* Code coverage can be measured and improved.
* Tests are organized by type, facilitating maintenance and selective execution.

---

¿Quieres que lo formatee también como archivo Markdown (`.md`) para documentación o sistema de ADRs como [adr-tools](https://github.com/npryce/adr-tools)?
