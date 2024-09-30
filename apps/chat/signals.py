from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import EventGroupMessage, UserGroupMessage
from apps.events.models import Participant
from apps.notification.models import Notification


# for Group Message
@receiver(post_save, sender=EventGroupMessage)
def create_message_group_async(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = f"event_group_{instance.event.id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {"type": "send_message", "message": instance},
    )
    for participant in Participant.objects.filter(event=instance.event):
        Notification.objects.create(
            user=participant.user,
            message=f"New Message for Event Group: {instance.event.name} - {str(instance.text_content)[:25]}...",
        )


# for User Message
@receiver(post_save, sender=UserGroupMessage)
def create_message_users_async(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    group_name = f"chat_user"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {"type": "send_message", "message": instance},
    )
    Notification.objects.create(
        user=instance.receiver,
        message=f"New Message from {instance.sender.username} - {str(instance.text_content)[:50]}",
    )
