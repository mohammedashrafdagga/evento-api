from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


# generate Token , uuid and reset link
def generate_user_token(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = (
        f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
    )
    return reset_link


# send email to user
def send_email_to_user(user, reset_link):
    email_subject = "Password Reset Request"
    message = render_to_string(
        "password_reset_email.html",
        {
            "user": user,
            "reset_link": reset_link,
        },
    )

    send_mail(email_subject, message, settings.APP_EMAIL, [user.email])
