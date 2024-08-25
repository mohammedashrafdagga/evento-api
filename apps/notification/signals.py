from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


@receiver(post_save, sender=Notification)
def send_notification_to_websocket(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = f"user_{instance.user.id}"

    # Prepare notification to send to user
    notification_message = {
        "message": instance.message,
        "notification_type": instance.notification_type,
        "create_at": instance.create_at.isoformat(),
    }

    async_to_sync(channel_layer.group_send)(
        group_name, {"type": "send_notification", "notification": notification_message}
    )
