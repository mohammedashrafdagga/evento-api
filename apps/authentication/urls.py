from django.urls import path
from .views import (
    UserRegistrationView,
    ChangePasswordView,
    UserProfileView,
    LogoutView,
    CustomLoginAPIView,
    CustomRefreshLoginAPIView,
    SendPasswordResetEmailView,
    PasswordRestConfirmAPIView,
)


app_name = "auth-app"
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", CustomLoginAPIView.as_view(), name="login"),
    path("login/refresh/", CustomRefreshLoginAPIView.as_view(), name="refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "reset-password/", SendPasswordResetEmailView.as_view(), name="reset-password"
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        PasswordRestConfirmAPIView.as_view(),
        name="reset-password-confirm",
    ),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/edit/", UserProfileView.as_view(), name="edit-profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
