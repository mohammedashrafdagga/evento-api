from src.settings.base import *

# Allow Host
ALLOWED_HOSTS = ["*"]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL USER TO SEND EMAIL
APP_EMAIL = os.environ.get("APP_EMAIL", "no-reply@yourdomain.com")


# normal data
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
# Postgresql for Development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DEV_DB_NAME"),
        "USER": os.environ.get("DEV_DB_USERNAME"),
        "PASSWORD": os.environ.get("DEV_DB_PASSWORD"),
        "HOST": os.environ.get(
            "DEV_DB_HOST"
        ),  # Or the IP address of your PostgreSQL server
        "PORT": os.environ.get("DEV_DB_PORT"),  # Default PostgreSQL port
    }
}


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static_root"


# setup media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# adding channels-redis
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}
