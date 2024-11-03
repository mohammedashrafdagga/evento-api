from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/v1/auth/", include("apps.authentication.urls", namespace="auth-app")),
    path("api/v1/events/", include("apps.events.urls", namespace="event-app")),
    path(
        "api/v1/notifications/",
        include("apps.notification.urls", namespace="notification-app"),
    ),
    path("api/v1/ticket/", include("apps.ticket.urls", namespace="tickets-app")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("admin/", admin.site.urls),
]

# adding media urls
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
