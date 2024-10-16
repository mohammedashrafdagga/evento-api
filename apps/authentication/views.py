from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.utils.active_user import activate_user_account
from apps.authentication.utils.base import send_notification
from apps.authentication.utils.register_user import send_register_email
from apps.authentication.utils.change_password_user import (
    change_user_password,
    reset_user_password,
    send_reset_password_email,
)

from .serializers import (
    PasswordChangeSerializer,
    PasswordResetEmailSerializer,
    PasswordRestSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


@extend_schema(tags=["Users"])
class CustomLoginAPIView(TokenObtainPairView):
    pass


@extend_schema(tags=["Users"])
class CustomRefreshLoginAPIView(TokenRefreshView):
    pass


# user registration views
@extend_schema(tags=["Users"])
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # send activate email
            send_register_email(request=request, user=user)

            return Response(
                {"detail": "User registered successfully. Verify your registration.."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user registration views
@extend_schema(tags=["Users"])
class ActivateUserAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        # active user account and sending email and notification
        activate_user_account(
            uid=kwargs.get("uidb64", ""), token=kwargs.get("token", "")
        )
        # Optionally log the user in here, or send a response indicating success
        return Response(
            {"detail": "Activate User Account successfully."},
            status=status.HTTP_200_OK,
        )


# Change User Password
@extend_schema(tags=["Users"])
class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            # Success Change User Password
            change_user_password(
                user=request.user, new_password=serializer.validated_data["password"]
            )

            return Response(
                {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile View
@extend_schema(tags=["Users"])
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        send_notification(
            user=user,
            message="Successfully Update your info",
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


# Logout View
@extend_schema(tags=["Users"])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh_token"])
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )


# rest password request APIView
@extend_schema(tags=["Users"])
class SendPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = PasswordResetEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():

            user = User.objects.get(email=serializer.validated_data["email"])

            # send password Link
            send_reset_password_email(request=request, user=user)

            # return Response
            return Response(
                {"message": "Password rest email send successfully."},
                status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ResetPassword
@extend_schema(tags=["Users"])
class PasswordRestConfirmAPIView(generics.GenericAPIView):
    serializer_class = PasswordRestSerializer

    def post(self, request, *args, **kwargs):

        serializer = PasswordRestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                reset_user_password(
                    uid=kwargs.get("uidb64", ""),
                    token=kwargs.get("token", ""),
                    new_password=serializer.validated_data["password"],
                )

                return Response(
                    {"message": "Password reset successful."}, status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
