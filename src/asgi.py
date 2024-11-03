import logging
import os

from django.core.asgi import get_asgi_application

from src.settings import base

if base.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.deployment")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

asgi_application = get_asgi_application()

from apps.chat.routers import chat_websocket_urlpatterns
from apps.notification.routers import notification_websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

logger = logging.getLogger(__name__)

# make some logs for testing
logger.info("Starting Log File")
logger.info("Starting Building .....")
logger.info("Starting Running .....")

websocket_urlpatterns = notification_websocket_urlpatterns + chat_websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routes=websocket_urlpatterns))
        ),
    }
)
