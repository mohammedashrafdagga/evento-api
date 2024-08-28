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
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"


# Security Question for User
class SecurityQuestion(models.Model):
    QuestionChoices = (
        (
            "what the number of your family?",
            "What the number of your family?",
        ),
        (
            "what the name of your best friend?",
            "What the name of your best friend?",
        ),
        (
            "what the name of your first company work?",
            "What the name of your first company work?",
        ),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, choices=QuestionChoices)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question}"
