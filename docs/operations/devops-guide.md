# ⚙️ DevOps Guide

> [Disclaimer](../DISCLAIMER.md)

## 🎯 Objective

Document the practices for maintenance, scalability, and support of the API.

## 📈 Scalability

- Use of containers to facilitate horizontal scaling
- Separation of services (DB, API, cache) to scale them independently
- Implementation of caching (Redis) for frequent queries

## 💾 Backups

- Daily database backup with `pg_dump`
- Storage in secure buckets (AWS S3, Google Cloud Storage)
- Periodic restoration testing

## 📝 Logs

- Centralized logs with ELK stack or equivalent
- HTTP access and error logs
- Log retention according to company policies

## 🔧 Maintenance

- Periodic dependency updates
- Application of security patches
- Review and cleaning of historical data
- Monitoring and ticket resolution

## 🔐 Security

- Mandatory use of HTTPS
- Minimal roles and permissions for services and users
- Rotation of credentials and secrets
