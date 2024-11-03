from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


User = get_user_model()


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        WARNING = "warning", "Warning"
        INFO = "info", "Info"
        ERROR = "error", "Error"

    class NotificationStatus(models.TextChoices):
        READ = "read", "Read"
        UNREAD = "unread", "Unread"

    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.TextField()
    notification_type = models.CharField(
        max_length=10, choices=NotificationType.choices, default=NotificationType.INFO
    )
    status = models.CharField(
        max_length=6,
        choices=NotificationStatus.choices,
        default=NotificationStatus.UNREAD,
    )
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
