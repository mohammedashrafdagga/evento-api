from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.TextChoices):
        HOSTING = "hosting", "Hosting"
        NORMAL = "normal", "Normal User"

    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=10, choices=[("M", "Male"), ("F", "Female")], null=True, blank=True
    )
    country = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10, choices=UserType.choices, default=UserType.NORMAL
    )

    def __str__(self):
        return f"{self.username}"
