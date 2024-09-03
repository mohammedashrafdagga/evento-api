from .base import generate_uuid_and_token, send_email


def generate_reset_link(request, user):
    token, uid = generate_uuid_and_token(user=user)
    reset_link = f"{request.scheme}://{request.get_host()}/api/auth/reset-password-confirm/{uid}/{token}/"
    return reset_link


class UserPasswordResetServices:
    @staticmethod
    def change_password_email(user):
        send_email(
            context={
                "subject": "Change Password Successfully",
                "context": {
                    "user": user,
                },
                "template_name": "emails/PasswordChangeSuccessfully.html",
            },
        )

    @staticmethod
    def send_reset_password_email(request, user) -> None:
        link = generate_reset_link(request, user)
        send_email(
            context={
                "subject": "Reset Password Request",
                "context": {
                    "user": user,
                    "link": link,
                },
                "template_name": "emails/ResetPasswordRequest.html",
            },
        )

    @staticmethod
    def set_password(user, new_password):
        user.set_password(new_password)
        user.save()

    @staticmethod
    def reset_password_success_email(user):
        send_email(
            context={
                "subject": "Reset Password Successfully",
                "context": {
                    "user": user,
                },
                "template_name": "emails/ResetPasswordSuccessfully.html",
            },
        )
