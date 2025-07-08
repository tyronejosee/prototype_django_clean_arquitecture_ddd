# 🗺️ Project Roadmap

> This is a realistic example, not a definitive development plan.

## Q3 2025 (Jul–Sep)

**Objective:** Functional MVP with basic product and order management

* [x] Docker environment setup (web, db, adminer)
* [x] Clean Architecture and DDD foundation (modular structure)
* [x] Product, category, and stock model
* [x] CRUD for products via REST API (Django Rest Framework)
* [x] Data validations with Value Objects
* [x] CI: GitHub Actions for linting/testing
* [x] Pre-commit with Ruff, Black, isort
* [ ] Base technical documentation (WIP)
* [ ] Initial structured changelog

## Q4 2025 (Oct–Dec)

**Objective:** Full e-commerce operability (backend only)

* [ ] Order management (creation, cancellation, state flow)
* [ ] Shopping cart
* [ ] Authentication and authorization with roles (customer/admin)
* [ ] Pricing and discount logic
* [ ] Basic reports (sales, low stock)
* [ ] Seeds and fixtures for local development
* [ ] Automatic OpenAPI docs (Swagger)

## Q1 2026 (Jan–Mar)

**Objective:** Scalability, observability, extensibility

* [ ] Webhooks (orders, stock changes)
* [ ] Metrics system (Prometheus + optional Grafana)
* [ ] Structured logging
* [ ] External payment system (e.g. Transbank, Webpay)
* [ ] Validations with Zod + React/Next.js frontend (partial integration)

## Q2 2026 (Apr–Jun)

**Objective:** Multi-store and advanced profiles

* [ ] Multi-user store administration
* [ ] Reviews and ratings module
* [ ] Notifications (email, Discord, etc.)
* [ ] Change audit (django-simple-history or similar)
* [ ] B2B mode (clients with agreements and differentiated pricing)

> This roadmap will be refined based on business priorities and technical feedback. Each delivery will include associated documentation and tests.
