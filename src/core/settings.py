import sys
from datetime import timedelta
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "src"))

SECRET_KEY: bool = config("SECRET_KEY", default="change-me")

DEBUG: bool = config("DEBUG", default=True, cast=bool)

IS_RUNNING_PIPELINE: bool = config("IS_RUNNING_PIPELINE", default=False, cast=bool)

IS_RUNNING_PYTEST: bool = any("pytest" in arg or "test" in arg for arg in sys.argv)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

DJANGO_MODULES: list = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_MODULES: list = [
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

LOCAL_MODULES: list = [
    "src.modules.cart",
    "src.modules.catalog",
    "src.modules.common",
    "src.modules.marketing",
    "src.modules.orders",
    "src.modules.payments",
    "src.modules.users",
]

INSTALLED_APPS: list = DJANGO_MODULES + THIRD_PARTY_MODULES + LOCAL_MODULES

MIGRATION_MODULES: dict = {
    "cart": "src.modules.cart.infrastructure.migrations",
    "catalog": "src.modules.catalog.infrastructure.migrations",
    "marketing": "src.modules.marketing.infrastructure.migrations",
    "orders": "src.modules.orders.infrastructure.migrations",
    "payments": "src.modules.payments.infrastructure.migrations",
    "users": "src.modules.users.infrastructure.migrations",
}

MIDDLEWARE: list = [
    "corsheaders.middleware.CorsMiddleware",
    "src.modules.common.infrastructure.middleware.backpressure.BackpressureMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES: list = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "resources" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

if IS_RUNNING_PYTEST or IS_RUNNING_PIPELINE:
    DATABASES: dict = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
else:
    DATABASES: dict = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="grocery_db"),
            "USER": config("POSTGRES_USER", default="grocery_user"),
            "PASSWORD": config("POSTGRES_PASSWORD", default="grocery_password"),
            "HOST": config("POSTGRES_HOST", default="db"),
            "PORT": config("POSTGRES_PORT", default=5432),
        },
    }

if IS_RUNNING_PYTEST or IS_RUNNING_PIPELINE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "test-cache",
        }
    }
else:
    CACHES: dict = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config("CACHE_LOCATION"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        },
    }


AUTH_PASSWORD_VALIDATORS: list = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT: Path = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = False

THROTTLE_5_PER_MINUTE = "5/minute"
THROTTLE_10_PER_MINUTE = "10/minute"
THROTTLE_5_PER_HOUR = "5/hour"
THROTTLE_10_PER_HOUR = "10/hour"
THROTTLE_25_PER_HOUR = "25/hour"
THROTTLE_2_PER_DAY = "2/day"

MARKETING_THROTTLE_RATES: dict[str, str] = {
    "create_coupon": THROTTLE_5_PER_HOUR,
    "list_coupons": THROTTLE_5_PER_MINUTE,
    "create_promotion": THROTTLE_5_PER_HOUR,
    "list_promotions": THROTTLE_5_PER_MINUTE,
}

ORDERS_THROTTLE_RATES: dict[str, str] = {
    "create_order": THROTTLE_5_PER_HOUR,
    "list_orders": THROTTLE_5_PER_MINUTE,
    "retrieve_order": THROTTLE_5_PER_MINUTE,
    "cancel_order": THROTTLE_10_PER_HOUR,
}

REST_FRAMEWORK: dict = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    "DEFAULT_CONTENT_LANGUAGE": "en",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/minute",
        "user": "60/minute",
        **ORDERS_THROTTLE_RATES,
        **MARKETING_THROTTLE_RATES,
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "NUM_PROXIES": None,
    "PAGE_SIZE": 25,
    "SEARCH_PARAM": "q",
    "ORDERING_PARAM": "order",
}

SIMPLE_JWT: dict = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

CORS_ALLOWED_ORIGINS: list = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

PASSWORD_HASHERS: list = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com" if DEBUG else "https://api-m.paypal.com"
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID", default="secret-client-id")
PAYPAL_CLIENT_SECRET = config("PAYPAL_CLIENT_SECRET", default="secret-client-secret")
PAYPAL_RETURN_URL = config("PAYPAL_RETURN_URL", default="http://localhost:8000/payments/success")
PAYPAL_CANCEL_URL = config("PAYPAL_CANCEL_URL", default="http://localhost:8000/payments/cancel")


AUTH_USER_MODEL = "users.UserModel"

SPECTACULAR_SETTINGS: dict = {
    "TITLE": config("PROJECT_NAME", default="Grocery Store"),
    "VERSION": config("PROJECT_VERSION", default="1.0.0"),
    "DESCRIPTION": config("PROJECT_DESCRIPTION", default="Grocery Store API"),
    "LICENSE": {"name": config("LICENCE_NAME", default="None"), "url": config("LICENCE_URL", default="None")},
    "CONTACT": {"name": config("CONTACT_NAME", default="None"), "url": config("CONTACT_URL", default="None")},
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "REDOC_UI_SETTINGS": {"hideHostname": True, "theme": {"colors": {"primary": {"main": "#FF135B"}}}},
    "TAGS": [
        {"name": "health", "description": "Operations related to health checks"},
        {"name": "users", "description": "Operations related to users"},
        {"name": "catalog", "description": "Operations related to products"},
        {"name": "cart", "description": "Operations related to carts"},
        {"name": "orders", "description": "Operations related to orders"},
        {"name": "payments", "description": "Operations related to payments"},
        {"name": "marketing", "description": "Operations related to marketing"},
    ],
}
