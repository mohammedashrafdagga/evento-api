from django.db import models
from django.contrib.auth import get_user_model
from apps.events.models import Event

# user instance
User = get_user_model()


class EventGroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, related_name="messages", on_delete=models.CASCADE)
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(
        blank=True, null=True, upload_to="chat_group_images/"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to Event Group {self.event.name }"


# Message Model
class UserGroupMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(
        blank=True, null=True, upload_to="chat_users_images/"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
