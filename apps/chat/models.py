from django.contrib.auth import get_user_model
from django.db import models

from apps.events.models import Event

# user instance
User = get_user_model()

# Message
class Message(models.Model):
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(
        blank=True, null=True, upload_to="messages_image/"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "message"
        verbose_name = "Message"
        verbose_name_plural = "Messages"


# Group Message
class EventMessage(models.Model):
    event = models.OneToOneField(
        Event, related_name="messages", on_delete=models.CASCADE
    )
    messages = models.ManyToManyField(Message, related_name="event")

    def __str__(self):
        return f"Message Event for: {self.event.name}"

    class Meta:
        db_table = "event_message"
        verbose_name = "EventMessage"
        verbose_name_plural = "EventMessages"


class EventGroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(
        Event, related_name="event_messages", on_delete=models.CASCADE
    )
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(
        blank=True, null=True, upload_to="chat_group_images/"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to Event Group {self.event.name }"

    class Meta:
        db_table = "group_message"
        verbose_name = "GroupMessage"
        verbose_name_plural = "GroupMessages"


class UserGroupMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_user_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receive_user_messages",
    )
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(
        blank=True, null=True, upload_to="messages_image/"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "user_message"
        verbose_name = "UserMessage"
        verbose_name_plural = "UserMessages"


# User Model
class UserMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receive_messages"
    )
    messages = models.ManyToManyField(Message)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

    class Meta:
        unique_together = ("sender", "receiver")
        db_table = "user_messages"
        verbose_name = "UserMessages"
        verbose_name_plural = "UserMessages"
