from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("api/auth/", include("apps.authentication.urls", namespace="auth-app")),
    path("api/events/", include("apps.events.urls", namespace="event-app")),
    path(
        "api/notifications/",
        include("apps.notification.urls", namespace="notification-app"),
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("admin/", admin.site.urls),
]

# adding media urls
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
