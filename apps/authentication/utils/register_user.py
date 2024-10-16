import threading

from django.contrib.auth import get_user_model

from .base import generate_uuid_and_token, send_email

User = get_user_model()


def generate_activate_link(request, user: User) -> str:
    """
    Generate Link for Allow to User active account
    """
    token, uid = generate_uuid_and_token(user=user)
    return (
        f"{request.scheme}://{request.get_host()}/api/v1/auth/activate/{uid}/{token}/"
    )


def send_register_email(request, user: User) -> None:
    """
    Generates an activation link and sends it to the user's email.
    """
    link = generate_activate_link(request=request, user=user)
    context = (
        {
            "subject": "Activate User Account",
            "context": {
                "user": user,
                "link": link,
            },
            "template_name": "emails/ActivateUserAccount.html",
        },
    )
    threading.Thread(
        target=send_email,
        args=(context),
    ).start()
