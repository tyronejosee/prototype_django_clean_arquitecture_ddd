# AWS ElastiCache (ClickOps Version)

## ⚙️ Choose the engine and create the ElastiCache instance

1. Go to **AWS Console → ElastiCache → “Create cache.”**

2. **Engine:**
   * **Redis** — supports expirations, optional persistence, and advanced data structures.

3. **Configuration:**
   * **Cluster mode:** *Single node* for testing, or *Cluster mode enabled* for production.
   * **Node type:** `t3.micro` for development/testing.
   * **Number of nodes:** `1` for dev, `≥2` for production.

4. **Subnet group / VPC:** select the VPC where your Django app runs (same as RDS or EC2 if applicable).

5. Click **Create**.

> ⏳ Wait until the status changes to `available`.

## 🔒 Configure Security Groups

* Go to your **ElastiCache cluster → Security group**.
* Add an **inbound rule**:
  * **Type:** Custom TCP
  * **Port:**
    * Redis: `6379`
  * **Source:** your Django server’s IP or Security Group (EC2, ECS, Lambda).

> This ensures that only your application can connect to the cache.

## 🌐 Get the connection endpoint

* Go to **Configuration → Primary Endpoint (Redis)**.
* Save the endpoint and port to use in your Django app.

> Example: `mycache.abcd1234.0001.use1.cache.amazonaws.com:6379`

## 🧩 Update your environment variables

In your `.env` file:

```bash
REDIS_PORT=6379
CACHE_LOCATION=<elasticache-endpoint> # e.g., redis://mycachecluster.xxxxx.0001.use1.cache.amazonaws.com:6379/0
```

## 🧪 Test the connection

In the Django shell:

```bash
python manage.py shell
```

Then run:

```python
from django.core.cache import cache

cache.set("test_key", "hello world", timeout=60)
cache.get("test_key")  # should return "hello world"
```

✅ If this works, your integration is correctly configured.

## 🚀 Optional settings

* **Timeouts:** define a `timeout` depending on usage (e.g., `300` seconds = 5 minutes).
* **Eviction:** Redis supports strategies like *LRU* and *LFU*.
* **Persistence:** enable Redis snapshots (`RDB`) or *AOF* for production reliability.
* **Cluster mode:** recommended for high availability and scalability.
* **Monitoring:** use **CloudWatch** to track memory usage, cache hits, and misses.
