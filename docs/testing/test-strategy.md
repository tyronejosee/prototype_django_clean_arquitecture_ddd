# 🧪 Test Strategy

> [Disclaimer](../DISCLAIMER.md)

## 🎯 Objective

Ensure the quality, stability, and reliability of the grocery and food store API (similar to Líder, Chile) through an automated and manual testing strategy covering different levels: unit, integration, and end-to-end (E2E).

## 📏 Scope

This strategy applies to all modules of the API developed with Django REST Framework under a Clean Architecture with DDD.

## 🧩 Test Levels

### ✅ Unit Tests

* **Objective:** Validate isolated behavior of functions and methods.
* **Technology:** `pytest`, `unittest`, `pytest-django`
* **Coverage:**

  * Entities (Domain Models)
  * Value Objects and pure logic
  * Use cases (application services)
  * Validations

### 🔁 Integration Tests

* **Objective:** Validate interaction among multiple system components (e.g., adapters ↔ use cases ↔ DB).
* **Technology:** `pytest`, `factory_boy`, `django.db`, real PostgreSQL DB with Docker.
* **Coverage:**

  * Repositories
  * Serializers and views (Views/API controllers)
  * REST endpoints

### 🌐 End-to-End (E2E) Tests

* **Objective:** Validate complete flows as a real consumer would.
* **Technology:** `pytest`, `httpx`, `requests`, validation scripts against Docker environment.
* **Coverage:**

  * Registration and login
  * Purchase flow
  * Checkout and payment (simulated)
  * Inventory management

## 🤖 Automation

* Tests run on every `push` and `pull_request` in GitHub Actions.
* Execution strategy:

  * `unit` and `integration`: on every commit.
  * `e2e`: on staging environment (on demand or merge to `main`).

## 🛠️ Tools

| Level         | Tool                                  |
| ------------- | ------------------------------------- |
| Unit          | `pytest`, `unittest`, `pytest-mock`  |
| Integration   | `factory_boy`, `pytest-django`        |
| E2E           | `httpx`, `requests`, Insomnia (manual) |
| Coverage      | `coverage.py`, `pytest-cov`           |
| Automation    | `GitHub Actions`                      |

## 📚 Conventions

* All tests must be in files named `test_*.py`.
* Structure reflects DDD modules: `domain/`, `application/`, `infrastructure/`, `interface/`.
* Mocks only in unit tests. Integration tests use real DB.
* Descriptive names following `given-when-then` pattern inside test bodies.

## 🎯 Goals

* ✅ Minimum coverage: `80%` lines.
* ✅ Execution time: < 2 minutes for CI.
* ❗ E2E tests separated to avoid friction during development.

## 👥 Responsible Roles

* QA / Developers responsible for unit and integration tests.
* Lead Engineer validates minimum coverage before merging to `main`.

## 📝 Final Notes

* Tests are integrated with `pre-commit` for basic validations (`ruff`, `black`, `isort`).
* Load testing planned for future (`Locust`, `k6`).
