# 📝 Changelog

> [Disclaimer](../DISCLAIMER.md)
> Maintained manually. Based on conventions like [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] — 2025-07-05

### Added

* Project base with Clean Architecture + DDD
* Docker Compose container setup: `web`, `db`, `adminer`
* Environment setup with pre-commit (`ruff`, `black`, `isort`, `end-of-file-fixer`)
* GitHub Actions for CI: lint + test
* `catalog` app with models:

  * `Product`
  * `Category`
* Initial validations in entities using Value Objects (UUID, Price, Stock)
* Basic CRUD via DRF for products and categories
* Admin enabled for catalog models

## [0.2.0] — 2025-07-12 *(planned)*

### Added

* Auth (users, login, basic roles)
* Endpoints protected by permissions
* Initial seeders for local development
* Automatically generated Swagger documentation

### Changed

* Environment configuration split (`base.py`, `local.py`, `production.py`)
* Renamed `views.py` to `controllers.py` for style consistency

> The following changes should be recorded at each merge or release.
