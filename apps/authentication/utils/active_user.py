import threading

from django.contrib.auth import get_user_model

from .base import send_email, send_notification, validate_token, validate_uid

# user instance Model
User = get_user_model()


# sending email for user when active account
def send_active_user_email(user):
    context = {
        "subject": " Successfully Activate Your Account",
        "template_name": "emails/AccountActivationSuccessfully.html",
        "context": {"user": user},
    }
    threading.Thread(
        target=send_email,
        args=(context),
    ).start()


def activate_user_account(uid: str, token: str) -> None:
    # validate uid and token
    user = validate_uid(uid)
    validate_token(user, token=token)

    # active user
    user.is_active = True
    user.save()

    # send notification for user and email for active account
    send_notification(user=user, message="Activate Your Account Successfully")
    send_active_user_email(user)
