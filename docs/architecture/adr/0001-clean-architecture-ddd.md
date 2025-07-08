# ADR 0001: Clean Architecture and DDD

## Context

The project implements a Django application following the principles of Clean Architecture and Domain Driven Design (DDD). The goal is to achieve a clear separation of responsibilities, facilitate testing and maintainability, and decouple the domain from the infrastructure.

## Decision

- The code is structured in layers: Domain, Application, Infrastructure, and Presentation.
- Each layer has its own folder and well-defined responsibilities.
- The domain does not depend on frameworks or infrastructure details.
- Use cases coordinate business logic and orchestrate operations.
- Repositories abstract data access.
- Infrastructure implements technical details (ORM, admin, etc.).
- Presentation exposes the API (views, routers, serializers).

## Consequences

- The code is easier to test and maintain.
- The infrastructure (for example, the ORM) can be changed without affecting the domain.
- The learning curve is higher for new developers.
