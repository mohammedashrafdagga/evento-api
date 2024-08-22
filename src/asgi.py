import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.notification.routing import notification_websocket_urlpatterns


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(notification_websocket_urlpatterns)),
    }
)
