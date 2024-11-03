from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.TextChoices):
        HOSTING = "hosting", "Hosting"
        NORMAL = "normal", "Normal User"

    first_name = models.CharField(max_length=25, null=False)
    last_name = models.CharField(max_length=25, null=False)
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
    bio = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"


    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'