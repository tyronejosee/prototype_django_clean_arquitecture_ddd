# 🛠️ System Overview

> [Disclaimer](../DISCLAIMER.md)

## 🧭 Overview

This API represents the backend for a Chilean-style grocery and food store, similar to a supermarket. It implements principles of **Domain-Driven Design (DDD)** and **Clean Architecture** with the goal of maintaining technology independence, high maintainability, and separation of concerns.

## 🏗️ Architecture

The solution follows a concentric layered structure based on Clean Architecture:

```bash
folder/
├── manage.py
├── pyproject.toml / requirements/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py / wsgi.py
│
├── apps/
    └── <bounded-context>/
        ├── domain/
        │   ├── entities/
        │   ├── value_objects/
        │   ├── services/
        │   └── exceptions.py
        │
        ├── application/
        │   ├── use_cases/
        │   └── providers.py
        │
        ├── infrastructure/
        │   ├── migrations/
        │   ├── repositories/
        │   └── external_services/
        │
        └── presentation/
        │   └── controllers/
        │   └── serializers/
        │   └── urls.py
        │
        └── tests/

````

Each layer only depends on the inner ones and uses **explicit interfaces** to decouple implementations.

## ⚙️ Technology Stack

* **Main language:** Python 3.13
* **Web framework:** Django 5.2.x
* **API layer:** Django REST Framework
* **Database:** PostgreSQL
* **Containers:** Docker + Docker Compose
* **CI/CD:** GitHub Actions
* **Linting & Quality:** Pre-commit with Ruff, Black, isort, Bandit

## 🌐 Main Flows

### 1. Catalog

* Products listed by category, brand, availability
* Search by name or SKU

### 2. Orders

* Checkout, payments, purchase history
* Coupons, discounts, and tracking

### 3. Users

* Registration, login, account recovery
* Shipping addresses, preferences

### 4. Admin Panel (future)

* Extended CRUD on products, users, orders

## 🧩 External Integrations (planned)

* Payment services: Transbank / MercadoPago
* Notifications: Sendgrid / Firebase
* Monitoring: Sentry / Grafana + Prometheus

## ✅ Quality Goals

| Criterion                   | Target |
| --------------------------- | ------ |
| Coupling                    | Low    |
| Test coverage               | 80%+   |
| Infrastructure independence | High   |
| Multi-environment support   | Yes    |
| Modularity                  | High   |

## 📈 Initial Metrics (CI/CD)

* Pipelines: `test`, `lint`, `docker`, `deploy-preview`
* Deployment time: < 5 min
* Pre-commit: blocks PRs if lint/tests fail
