# AWS RDS (ClickOps Version)

## ⚙️ Choose the engine and create the RDS database

1. Go to the **AWS Console → RDS → “Create database.”**
2. Configure the following:
   * **Engine:** PostgreSQL (recommended), MySQL, or another option.
   * **Version:** whichever your app supports (e.g., PostgreSQL 15.x).
   * **Template:** choose *Production* or *Dev/Test* depending on your needs.
   * **DB instance identifier:** a unique name.
   * **Master username / password:** save these credentials—you’ll need them in Django.
   * **Instance class:** server size (use *t2.micro* or *db.t3.micro* for the free tier).
   * **Storage:** the default option is fine for development.

3. **Network:**
   * **VPC:** select the one you use (the default VPC is fine for testing).
   * **Public access:**
     * `Yes` if you need to connect from your local machine (development only).
     * `No` for production—access only within your VPC.

4. Click **Create database**.

> ⏳ Wait until the status changes to `available`.

## 🔒 Configure security (Security Group)

* Go to your **DB instance → Connectivity & Security → VPC security groups**.
* Open the port for your database engine:
  * PostgreSQL: `5432`
  * MySQL: `3306`

* Add an **inbound rule** for your development IP or the server running Django.
* For production within the same VPC, restrict access to the IP range of your EC2 / ECS / Lambda instances.

## 🌐 Get the connection details

In **RDS → Databases → your instance → Connectivity & Endpoint**, note the following:

* **Endpoint:** something like `mydb.abcd1234.us-east-1.rds.amazonaws.com`
* **Port:** `5432` (for PostgreSQL)
* **DB name:** the name of your database (you can create additional ones if needed)
* **Username / Password:** the credentials you defined when creating the DB

## 🧩 Update your environment variables

In your `.env` file:

```bash
POSTGRES_DB=<db-name>
POSTGRES_USER=<db-user>
POSTGRES_PASSWORD=<db-password>
POSTGRES_HOST=<db-host> # e.g., mydb.abcd1234.us-east-1.rds.amazonaws.com
POSTGRES_PORT=<db-port>
```

## 🧪 Test the connection

From your local machine:

```bash
python manage.py migrate
```

* If everything is correct, Django will apply the migrations to RDS.
* Then run `python manage.py createsuperuser` to verify that data insertion works.

## 🚀 Optional settings

* **SSL:** AWS RDS supports SSL connections—recommended for production.

  ```python
  DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}
  ```

* **Connection pool:** use `django-db-geventpool` or `pgbouncer` if your app handles high traffic.
* **Automatic backups:** configure them in RDS to prevent data loss.
* **Multi-AZ:** enables high availability (production only).
