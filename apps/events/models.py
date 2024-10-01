from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="tags"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"


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
