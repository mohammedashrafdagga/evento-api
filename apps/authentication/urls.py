from django.urls import path
from .views import UserRegistrationView, ChangePasswordView, UserProfileView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "auth"
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/edit/", UserProfileView.as_view(), name="edit-profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
