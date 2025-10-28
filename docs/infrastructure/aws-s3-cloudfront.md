# AWS S3 + CloudFront (ClickOps Version)

## 🪣 Create an S3 Bucket

1. Go to **AWS Console → S3 → “Create bucket.”**

2. Configure:
   * **Bucket name:** must be globally unique.
   * **Region:** same as your `AWS_S3_REGION_NAME`.
   * **Block public access:** depends on your use case:

     * For **public files** (CSS, JS, static images) → **disable** public access blocking.
     * For **private files** (user uploads) → **keep enabled** and use signed URLs in Django.

3. Click **Create bucket**.

## 🔒 Configure Bucket Permissions (Bucket Policy)

Depending on whether your content is public or private:

### ✅ Public (static files)

Example of a minimal public-read policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<bucket-name>/*"
    }
  ]
}
```

> Replace `<bucket-name>` with your actual bucket name.

### 🔐 Private (media uploads)

* You don’t need a public policy.
* Django will handle **signed URLs** if `AWS_QUERYSTRING_AUTH = True`.

## 👤 Create an IAM User for Django

### In AWS → **IAM → Users → Add user**

* **User name:** e.g., `django-s3-user`
* **Access type:** **Programmatic access** (access key + secret key)

### Assign permissions

Use an **inline** or **managed** policy. Example of a minimal inline policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::<bucket-name>"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": ["arn:aws:s3:::<bucket-name>/*"]
    }
  ]
}
```

> This allows Django to list, upload, and delete objects **only in your bucket**, not globally.

✅ Save the **`AWS_ACCESS_KEY_ID`** and **`AWS_SECRET_ACCESS_KEY`** — you’ll use them in your `.env` file.

## 🌐 Configure CORS (if accessed directly from frontend)

* Go to your **bucket → Permissions → CORS configuration → Edit.**
* Example setup:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

> Change `AllowedOrigins` to your frontend domain for better security.

## ⚙️ Configure Django with your credentials

In your `.env`:

```bash
DEBUG=False  # production

AWS_ACCESS_KEY_ID=<aws-access-key>
AWS_SECRET_ACCESS_KEY=<aws-secret-key>
AWS_STORAGE_BUCKET_NAME=<aws-bucket-name>
AWS_S3_REGION_NAME=<aws-region-name>
AWS_S3_CUSTOM_DOMAIN=<aws-cloudfront-domain>
```

Then, in your `settings.py`:

```python
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", "us-east-1")
AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN", f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com")
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_LOCATION = "static"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=31536000"}  # 1 year
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = True

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "location": "static",
        },
    },
}

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
```

## 🧪 Run Collectstatic and Test

```bash
python manage.py collectstatic
```

* Your static files should now be uploaded to the S3 bucket.
* Test uploading a file via a Django model with a `FileField` (e.g., `Product.image`) to verify **media uploads** also go to S3.

## 🚀 Configure CloudFront (CDN) — Optional but Recommended

### 🌍 Create a CloudFront Distribution

1. Go to **AWS → CloudFront → Create distribution → Web.**
2. Basic setup:

   * **Origin domain:** your S3 bucket (use the raw S3 endpoint, no `https://` prefix).

     ```bash
     <bucket-name>.s3.amazonaws.com
     ```

   * **Origin path (optional):** leave empty or set `static` to point only to static files.
   * **Viewer Protocol Policy:** `Redirect HTTP to HTTPS` (recommended).
   * **Allowed HTTP Methods:** `GET, HEAD` for static content; add `OPTIONS` for CORS.
   * **Cache policy:** use **Managed-CachingOptimized** or a custom one with specific TTLs.

### 🧱 Configure CORS and Headers

* If files are accessed from another domain (e.g., frontend), enable **CORS headers**.

  * Go to **Behaviors → Edit → Response Headers Policy**, and choose `CORS-S3Origin` or create your own.
* For **private files** (signed URLs), ensure **Query String Forwarding** is enabled so CloudFront passes authentication parameters.

### 🔐 Enable SSL / HTTPS

* If using a custom domain (e.g., `cdn.yourdomain.com`):

  * Add it under **Alternate Domain Names (CNAMEs)**.
  * Attach a certificate from **AWS Certificate Manager (ACM)** — free via AWS.

### ⚙️ Update Django for CloudFront

In your `.env`:

```bash
AWS_S3_CUSTOM_DOMAIN=d123abcxyz.cloudfront.net  # CloudFront domain
```

Your existing `STATIC_URL` and `MEDIA_URL` will automatically point to your CDN:

```python
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
```

### ♻️ Invalidate Cache (optional)

When files are updated in S3, CloudFront might still serve cached versions.
You can invalidate manually via the console or programmatically using boto3:

```python
import boto3, time

client = boto3.client('cloudfront')
client.create_invalidation(
    DistributionId='DISTRIBUTION_ID',
    InvalidationBatch={
        'Paths': {'Quantity': 1, 'Items': ['/*']},
        'CallerReference': str(time.time())
    }
)
```

✅ With this setup, your **static and media files** will be served globally through **CloudFront**, improving performance and reliability.
