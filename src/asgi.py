import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from apps.notification.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
