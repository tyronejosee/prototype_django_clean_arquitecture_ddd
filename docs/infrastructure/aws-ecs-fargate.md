# AWS ECS, Registry and Fargate (ClickOps Version)

## ✅ Prerequisites

You should already have:

* AWS Account and CLI configured (`aws configure`)
* Docker and `docker-compose` installed locally
* RDS (PostgreSQL) created
* ElastiCache (Redis) created
* S3 bucket + CloudFront configured for static and media files

## 🧪 Test Locally (Optional)

```bash
docker build -t marketly .
docker run -p 8000:8000 marketly
```

Verify it works: [http://localhost:8000](http://localhost:8000)

## 🪣 Push Image to **Amazon ECR (Elastic Container Registry)** (Optional)

> This is just an example using ECR.
> In production, your GitHub Actions pipeline automatically pushes the image to Docker Hub whenever you push to `main`.

1. **Create the repository in ECR:**

   ```bash
   aws ecr create-repository --repository-name marketly
   ```

2. **Log in to ECR:**

   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
   ```

3. **Tag and push the image:**

   ```bash
   docker tag marketly:latest <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/marketly:latest
   docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/marketly:latest
   ```

## 🐝 Create an **ECS Cluster**

In AWS Console → **ECS → Clusters → Create Cluster**

* Choose: **Fargate** (serverless, no need for EC2)
* Name: `marketly-cluster`
* VPC: the same one used by RDS and Redis
* Subnets: public or private (depending on your architecture)
* Security Group: allow outbound Internet access and inbound access if using a load balancer

## 🧭 Create a **Task Definition**

In ECS → Task Definitions → “Create new task definition”:

* **Launch type:** Fargate
* **Container name:** `marketly-app`
* **Image:**
  `<aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/marketly:latest`
* **Port mappings:** `8000 → 8000`
* **CPU / Memory:** minimum `0.5 vCPU / 1GB RAM`

> 💡 Ideally, load these variables from **AWS SSM Parameter Store** or **Secrets Manager**, not directly in the task definition.

## 🌐 Configure Networking and Security

Make sure that:

* The **ECS Task** is in the same **VPC and subnets** as RDS and Redis
* The **ECS Security Group** allows outbound traffic to ports `5432` (RDS) and `6379` (Redis)
* RDS and Redis **allow inbound traffic** from the ECS Security Group

## 🔄 Create the **ECS Service**

In ECS → Clusters → `marketly-cluster` → **Services → Create**

* **Launch type:** Fargate
* **Task definition:** the one created earlier
* **Desired tasks:** 1 or more
* **Load Balancer:**
  * If using **CloudFront + API Gateway** → ❌ not required
  * If you want direct access → ✅ use an **Application Load Balancer (ALB)**
* Enable **Auto Scaling** if needed

## ☁️ Integration with CloudFront and S3

Your **CloudFront** serves **static and media files**, while your **ECS** handles only **dynamic (API) requests**.

In your `settings.py`:

```python
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
```

> ⚠️ Django **should not serve static files** in production — that’s handled by **S3 + CloudFront**, separate from your ECS container.
