from .base import generate_uuid_and_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from apps.notification.models import Notification
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import exceptions
from django.contrib.auth.tokens import default_token_generator
from .base import send_email

User = get_user_model()


def generate_activate_link(request, user) -> str:
    """
    Generate Link for Allow to User active account
    """
    token, uid = generate_uuid_and_token(user=user)
    return f"{request.scheme}://{request.get_host()}/api/auth/activate-account/{uid}/{token}/"


class UserRegistrationService:

    """
    Service class for user registration related actions.
    """

    @staticmethod
    def send_activation_email(user, request):
        """
        Generates an activation link and sends it to the user's email.
        """
        link = generate_activate_link(request=request, user=user)
        send_email(
            context={
                "subject": "Activate User Account",
                "context": {
                    "user": user,
                    "link": link,
                },
                "template_name": "emails/ActivateUserAccount.html",
            },
        )

    @staticmethod
    def create_notification(user):
        """
        Creates a notification for the user.
        """
        Notification.objects.create(user=user, message="Success Create Your Account")


class UserActiveAccountServices:
    @staticmethod
    def validate_uid(uid):
        """Validate Uidb64 is Correct"""
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise exceptions.ValidationError("Invalid UID")

    @staticmethod
    def validate_token(user, token):
        """Check the Token is correct for User"""
        if not default_token_generator.check_token(user, token):
            raise exceptions.ValidationError("Invalid or expired token.")

    @staticmethod
    def activate_user(user):
        """Active User Account"""
        user.is_active = True
        user.save()

    @staticmethod
    def send_notification(user):
        """
        generate notification for success active user account
        """
        Notification.objects.create(user=user, message="Success Activate Your Account")

    @staticmethod
    def activate_user_success_email(user):
        send_email(
            context={
                "subject": " Successfully Activate Your Account",
                "template_name": "emails/AccountActivationSuccessfully.html",
                "context": {"user": user},
            },
        )
