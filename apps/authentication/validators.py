from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


def validate_email_is_exists(value):
    """
    We Have Two validation for email :
    - Frontend (valid if the user write the valid email correctly)
    - Backend (if the user enter the email not exists already)
    """
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("A user with this email already exists.")
    return value


def validate_email_is_not_exists(value):
    """
    We Have Two validation for email :
    - Frontend (valid if the user write the valid email correctly)
    - Backend (if the user enter the email not exists already)
    """
    if not User.objects.filter(email=value).exists():
        raise serializers.ValidationError("A user with this email not  exists.")
    return value


def validate_passwords(data):
    """
    Validate that the new password and confirm password match.
    """
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    if password != confirm_password:
        raise serializers.ValidationError("Passwords do not match.")

    return data


def validate_change_password(user, data):
    old_password = data.get("old_password")

    if not user.check_password(old_password):
        raise serializers.ValidationError(
            {"old_password": "Old password is not correct."}
        )

    return validate_passwords(data=data)
