from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("api/auth/", include("apps.authentication.urls", namespace="auth")),
    path("admin/", admin.site.urls),
]

# adding media urls
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)