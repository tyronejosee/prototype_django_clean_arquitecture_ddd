# Objective

```mermaid
graph TD
    %% === Users and public layers ===
    User["User"] -->|HTTP/HTTPS| CF[CloudFront CDN]
    CF -->|Static files and media| S3["Amazon S3 Bucket"]

    User -->|HTTP/HTTPS| ALB["Application Load Balancer"]

    %% === VPC and subnets ===
    subgraph VPC["AWS VPC"]
        subgraph Public["Public Subnets"]
            ALB --> ECS["ECS Service Fargate With APP"]
        end

        subgraph Private["Private Subnets"]
            ECS -->|PostgreSQL| RDS["Amazon RDS PostgreSQL"]
            ECS -->|Cache| Redis["Amazon ElastiCache Redis"]
        end
    end

    %% === Security, roles y secrets ===
    Secrets["AWS Secrets Manager"] --> ECS
    ParamStore["AWS SSM Parameter Store"] --> ECS
    IAMRole["IAM Role ECS Task Execution"] --> ECS
    IAMRole --> S3
    IAMRole --> RDS
    IAMRole --> Redis
    IAMRole --> Secrets


    %% === Logs and monitoring ===
    ECS --> CW["Amazon CloudWatch Logs"]

    %% === Visual styles ===
    classDef cloud fill:#f0f9ff,stroke:#0369a1,stroke-width:1px,color:#000;
    classDef compute fill:#ecfdf5,stroke:#047857,stroke-width:1px,color:#000;
    classDef storage fill:#fef3c7,stroke:#b45309,stroke-width:1px,color:#000;
    classDef service fill:#eef2ff,stroke:#4338ca,stroke-width:1px,color:#000;

    class CF,S3,ALB,Secrets,ParamStore,CW cloud;
    class ECS compute;
    class RDS,Redis storage;
    class IAMRole service;

```

- CloudFront + S3 → serve your static and media files through a global CDN.
- Application Load Balancer (ALB) → exposes your application to the public.
- ECS (Fargate) → runs your app in serverless containers.
- RDS (PostgreSQL) → managed relational database.
- ElastiCache (Redis) → cache layer for API endpoints.
- Secrets Manager / Parameter Store → store credentials and configuration (optional).
- IAM Role → grants secure permissions without hard-coded keys.
- CloudWatch → centralized logging and monitoring.
