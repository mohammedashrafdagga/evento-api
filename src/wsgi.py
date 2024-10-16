import os

from django.core.wsgi import get_wsgi_application
from src.settings import base

if base.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.deployment")

application = get_wsgi_application()
