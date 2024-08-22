from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# event Model
class Event(models.Model):
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_events",
        limit_choices_to={"user_type": "hosting"},
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
    participants = models.ManyToManyField(
        User,
        related_name="joined_events",
        blank=True,
    )

    def __str__(self):
        return self.name


class Section(models.Model):
    event = models.ForeignKey(Event, related_name="sections", on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField()
    speaker = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
