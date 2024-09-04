from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import (
    UserRegistrationSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    PasswordResetEmailSerializer,
    PasswordRestSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .utils.user_password import UserPasswordResetServices
from apps.authentication.utils.user_register import (
    UserRegistrationService,
    UserActiveAccountServices,
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
            # send activate email and notification for user
            UserRegistrationService.send_activation_email(request=request, user=user)
            UserRegistrationService.create_notification(user=user)

            # Optionally log the user in here, or send a response indicating success
            return Response(
                {"detail": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user registration views
@extend_schema(tags=["Users"])
class ActivateUserAPIView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):

        user = UserActiveAccountServices.validate_uid(kwargs.get("uidb64", ""))
        UserActiveAccountServices.validate_token(user, kwargs.get("token", ""))
        UserActiveAccountServices.activate_user(user)
        UserActiveAccountServices.send_notification(user)
        UserActiveAccountServices.activate_user_success_email(user=user)
        # Optionally log the user in here, or send a response indicating success
        return Response(
            {"detail": "Activate User Account successfully."},
            status=status.HTTP_200_OK,
        )


# Change User Password
@extend_schema(tags=["Users"])
class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():

            UserPasswordResetServices.set_password(
                user=request.user, new_password=serializer.validated_data["password"]
            )
            UserPasswordResetServices.change_password_email(user=request.user)
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
            UserPasswordResetServices.send_reset_password_email(request, user)

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
                user = UserActiveAccountServices.validate_uid(kwargs.get("uidb64", ""))
                UserActiveAccountServices.validate_token(user, kwargs.get("token", ""))
                UserPasswordResetServices.set_password(
                    user, serializer.validated_data["password"]
                )
                UserPasswordResetServices.reset_password_success_email(user=user)

                return Response(
                    {"message": "Password reset successful."}, status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
