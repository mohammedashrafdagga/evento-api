import threading

from django.contrib.auth import get_user_model

from .base import (generate_uuid_and_token, send_email, send_notification,
                   validate_token, validate_uid)


def generate_reset_password_link(request, user):
    token, uid = generate_uuid_and_token(user=user)
    reset_link = f"{request.scheme}://{request.get_host()}/api/v1/auth/reset-password-confirm/{uid}/{token}/"
    return reset_link


def send_reset_password_email(request, user) -> None:
    link = generate_reset_password_link(request, user)
    context = {
        "subject": "Reset Password Request",
        "context": {
            "user": user,
            "link": link,
        },
        "template_name": "emails/ResetPasswordRequest.html",
    }
    threading.Thread(target=send_email, args=(context)).start()


def reset_password_success_email(user: get_user_model()) -> None:
    context = {
        "subject": "Reset Password Successfully",
        "context": {
            "user": user,
        },
        "template_name": "emails/ResetPasswordSuccessfully.html",
    }
    threading.Thread(
        target=send_email,
        args=(context),
    ).start()


# stetting password for user
def set_password(user: get_user_model(), new_password: str) -> None:
    user.set_password(new_password)
    user.save()


def send_change_password_email(user: get_user_model()) -> None:
    context = {
        "subject": "Change Password Successfully",
        "context": {
            "user": user,
        },
        "template_name": "emails/PasswordChangeSuccessfully.html",
    }
    threading.Thread(
        target=send_email,
        args=(context),
    ).start()


# Allow to user to change password (View - Logic)
def change_user_password(user: get_user_model(), new_password: str) -> None:
    # set new password
    set_password(user, new_password)
    # sending email and notification for User
    send_change_password_email(user=user)
    send_notification(user=user, message="Successfully reset password")


def reset_user_password(uid: str, token: str, new_password: str) -> None:
    # validate uid and token 
    user = validate_uid(uid = uid)
    validate_token(token = token)
    
    # set new password 
    set_password(new_password)
    
    # send email and notification for success reset
    reset_password_success_email(user = user)
    send_notification(user=user, message="Successfully reset password")
