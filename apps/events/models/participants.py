from django.contrib.auth import get_user_model
from django.db import models

from .events import Event

# user model
User = get_user_model()


# We Split Adding All Participant in ALl Event
class Participant(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="participants",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        related_name="event_joined",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    join_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.event} - {self.user.username}"

    class Meta:
        db_table = "participants"
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
