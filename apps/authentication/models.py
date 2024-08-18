from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=10, choices=[("M", "Male"), ("F", "Female")], null=True, blank=True
    )
    country = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username}"
