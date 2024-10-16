from apps.notification.models import Notification
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import exceptions

# user model instance
User = get_user_model()

# generate UUID and Token for User
def generate_uuid_and_token(user: User):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return token, uid


# send email to user for reset password
def send_email(context: dict):
    message = render_to_string(context["template_name"], context=context["context"])
    send_mail(
        context["subject"],
        message,
        settings.APP_EMAIL,
        [context["context"].get("user").email],
    )


def send_notification(user: User, message: str):
    """
    generate notification for success active user account
    """
    Notification.objects.create(user=user, message=message)


def validate_uid(uid) -> User:
    """Validate Uidb64 is Correct"""
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
        return user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise exceptions.ValidationError("Invalid UID")


def validate_token(user: User, token: str) -> None:
    """Check the Token is correct for User"""
    if not default_token_generator.check_token(user, token):
        raise exceptions.ValidationError("Invalid or expired token.")
