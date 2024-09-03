from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import (
    validate_email_is_exists,
    validate_email_is_not_exists,
    validate_passwords,
    validate_change_password,
)


User = get_user_model()


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
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=str(validated_data["email"]).split("@")[0],
        )
        user.set_password(password)
        user.save()
        return user


# Change user Password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        return validate_change_password(user=self.context["request"].user, data=data)

    


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
            "profile_image",
        ]
        extra_kwargs = {
            "username": {"read_only": True},  # Prevent username from being updated
            "email": {"read_only": True},  # Prevent email from being updated if needed
            "user_type": {"read_only": True},
        }


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
