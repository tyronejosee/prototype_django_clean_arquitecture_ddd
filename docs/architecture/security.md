# 🔐 Security

> [Disclaimer](../DISCLAIMER.md)

## 🛡️ Key Principles

* **Defense in depth**: multiple layers of protection
* **Principle of least privilege**: minimum necessary access
* **Fail securely**: errors do not expose sensitive information
* **Secure by default**: all insecure features are explicitly disabled

## 🔐 Authentication and Authorization

### 🔹 Authentication

* JWT (`access` and `refresh` tokens)
* HTTP-Only + Secure cookies for frontend (pending)
* Token validation on every request

### 🔹 Authorization

* Roles (`admin`, `client`)
* Endpoint-level validation (`permissions.py`)
* User filters in queries

## 🔒 Data Protection

* All passwords encrypted with `PBKDF2` (default in Django)
* Sensitive data like credit cards are not stored
* Auditable logs but without PII data

## 🧱 Infrastructure Hardening

### Docker

* Images based on `python:3.11-slim`
* No root user inside containers
* Secure environment variables via `.env`

### Database

* User roles per environment (`dev`, `staging`, `prod`)
* Encrypted connections with TLS
* Automated daily backups

### Django

* `SECURE_SSL_REDIRECT = True`
* `SECURE_HSTS_SECONDS = 31536000`
* `SESSION_COOKIE_SECURE = True`
* `CSRF_COOKIE_SECURE = True`
* Active middleware: `SecurityMiddleware`, `XSSProtection`

## 🔎 Validation and Sanitization

* Thorough validation with `serializers` and `pydantic/zod` on frontend
* Sanitization of suspicious inputs (HTML, JS)
* Active protections against:

  * SQL Injection
  * XSS
  * CSRF (tokens + cookies)

## 🧪 Security Testing

* Automated scans with `bandit`
* `ruff` linter with active `S10x` rules
* CI/CD validations: merges are blocked if failures detected
* Dependabot active to update insecure packages

## 📉 Known Risks

* If using Django Admin, restrict by IP and VPN
* Webhooks must be validated with HMAC + timestamps
* Monitor for possible brute-force login attempts

## 📘 Future Recommendations

* Integrate WAF (Cloudflare, AWS)
* Support for WebAuthn
* Logging with anonymization (PII Masking)
* Auto-rotate secrets and keys
