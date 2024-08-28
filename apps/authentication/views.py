from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, generics, exceptions
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
from .utils import (
    generate_user_token,
    reset_email_to_user,
    email_for_activate_user_account,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from apps.notification.models import Notification

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
            # send email for user to activate account
            activate_link = generate_user_token(request, user)
            email_for_activate_user_account(user, activate_link=activate_link)
            # send notification for user
            Notification.objects.create(
                user=user, message="Success Create Your Account"
            )
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
        uidb64 = kwargs.get("uidb64", "")
        token = kwargs.get("token", "")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise exceptions.ValidationError("Invalid UID")

        if not default_token_generator.check_token(user, token):
            raise exceptions.ValidationError("Invalid or expired token.")

        user.is_active = True
        user.save()

        # create Success Activate Account for User
        Notification.objects.create(user=user, message="Success Activate Your Account")
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
            serializer.save()
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
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
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
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # generate Token and Send Email
            reset_link = generate_user_token(request, user)
            # send email to user
            reset_email_to_user(user=user, reset_link=reset_link)
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
                uidb64 = kwargs.get("uidb64", "")
                token = kwargs.get("token", "")
                serializer.save(uidb64, token)
                return Response(
                    {"message": "Password reset successful."}, status.HTTP_200_OK
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
