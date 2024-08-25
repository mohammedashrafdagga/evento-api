from django.urls import path
from .views import UserNotificationListAPIView, MarkNotificationAsReadView


app_name = "notification-app"


urlpatterns = [
    path(
        "list/",
        UserNotificationListAPIView.as_view(),
        name="user_notifications",
    ),
    path(
        "read/<int:pk>/",
        MarkNotificationAsReadView.as_view(),
        name="mark_notification_as_read",
    ),
]
