from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import (
    validate_change_password,
    validate_email_is_exists,
    validate_email_is_not_exists,
    validate_passwords,
)

User = get_user_model()

# ModelJobSerializer -> Way to rename serializer class
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email_is_exists])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        """
        - validate The Password and confirm_password if same or not
        """
        return validate_passwords(data)

    def create(self, validated_data):
        password = validated_data.pop("confirm_password", None)
        user = User.objects.create(
            first_name=str(validated_data["first_name"]).lower(),
            last_name=str(validated_data["last_name"]).lower(),
            email=str(validated_data["email"]).lower(),
            username=str(validated_data["email"]).split("@")[0].lower(),
        )
        user.set_password(password)
        user.save()
        return user


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "dob",
            "sex",
            "user_type",
            "country",
            "bio",
            "profile_image",
        ]
        extra_kwargs = {
            "username": {"read_only": True},  # Prevent username from being updated
            "email": {"read_only": True},  # Prevent email from being updated if needed
            "user_type": {"read_only": True},
        }


# Change user Password
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        return validate_change_password(user=self.context["request"].user, data=data)


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validate_email_is_not_exists])


class PasswordRestSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate The Token , UID, match for password and confirm password
        """
        return validate_passwords(data=data)


class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("name", "username", "bio", "profile_image")

    def get_name(self, obj) -> str:
        return f"{obj.first_name} {obj.last_name}"
