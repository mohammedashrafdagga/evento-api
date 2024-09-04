from rest_framework import serializers
from .models import Notification


# Notification Services
class NotificationService:
    @staticmethod
    def read_notification(notification):
        notification.status = Notification.NotificationStatus.READ
        notification.save()
