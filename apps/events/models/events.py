from django.contrib.auth import get_user_model
from django.db import models

from .categories import Category

# user model
User = get_user_model()

# event Model
class Event(models.Model):
    class AvailabilityChoices(models.TextChoices):
        all = "all", "All Users"
        specific = "specific", "Specific Users"

    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_events",
        limit_choices_to={"user_type": "hosting"},
    )
    category = models.ForeignKey(
        Category,
        related_name="events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(
        upload_to="event_images/", null=True, blank=True
    )
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    availability = models.CharField(
        max_length=10,
        choices=AvailabilityChoices.choices,
        default=AvailabilityChoices.all,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "events"
        verbose_name = "Event"
        verbose_name_plural = "Events"
