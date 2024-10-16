from src.settings.base import *

# Allow Host
ALLOWED_HOSTS = ["*"]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL USER TO SEND EMAIL
APP_EMAIL = os.environ.get("APP_EMAIL", "no-reply@yourdomain.com")

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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
