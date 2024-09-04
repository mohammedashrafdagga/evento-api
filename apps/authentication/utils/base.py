from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def generate_uuid_and_token(user):
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
