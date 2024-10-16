import pytest
from apps.notification.models import Notification
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

# User Model Instance
User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    def setup_method(self):
        # Initialize the API client to be used in each test
        self.client = APIClient()
        self.url = reverse(
            "auth-app:register"
        )  # Update with the correct URL for your registration endpoint

    def test_register_non_complete_data(self):
        #  'first_name': 'testuser',
        # 'last_name': 'system'
        data = {
            "password": "testpassword@testuser.com",
            "confirm_password": "testpassword@testuser.com",
            "email": "testuser@testuser.com",
        }
        # Send the POST request to register the user
        response = self.client.post(self.url, data)

        # Assert that the registration was successful
        assert response.status_code == 400  # Assuming 201 Created
        assert not User.objects.filter(email="john@example.com").exists()

    def test_register_complete_data(self):

        data = {
            "password": "testpassword@testuser.com",
            "confirm_password": "testpassword@testuser.com",
            "email": "testuser@testuser.com",
            "first_name": "testuser",
            "last_name": "system",
        }
        # Send the POST request to register the user
        response = self.client.post(self.url, data)

        # Assert that the registration was successful
        assert response.status_code == 201  # Assuming 201 Created
        assert (
            User.objects.filter(email="testuser@testuser.com").first().username
            == "testuser"
        )
        assert not User.objects.get(email="testuser@testuser.com").is_active

    def test_register_existing_email(self):
        # Step 1: Create a user manually using Django ORM
        User.objects.create_user(
            username="existing_user", email="john@example.com", password="password123"
        )

        # Step 2: Attempt to register another user with the same email
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john@example.com",  # Same email as the existing user
            "password": "password123",
            "confirm_password": "password123",
        }

        response = self.client.post(self.url, data)

        # Step 3: Assert that the registration fails due to duplicate email
        assert response.status_code == 400  # Assuming 400 Bad Request
        assert "email" in response.data  # Check if email error is present
        assert (
            "already exists" in str(response.data["email"]).lower()
        )  # Customize based on your error message


# test login and get access_and token
@pytest.mark.django_db
class TestUserLogin:
    def setup_method(self):
        # Initialize the API client and login URL
        self.client = APIClient()
        self.url = reverse(
            "auth-app:login"
        )  # Replace with the correct URL for login endpoint

        # Create a user to be used in the login tests
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123",
            is_active=True,
        )

    # TEST Success Login
    def test_login_success(self):
        data = {"username": "john", "password": "password123"}

        # Send POST request to the login endpoint
        response = self.client.post(self.url, data)
        # Assert that the login is successful
        assert response.status_code == 200  # Assuming 200 OK for successful login
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self):
        # Incorrect password
        data = {"username": "john", "password": "wrongpassword"}

        # Send POST request to the login endpoint
        response = self.client.post(self.url, data)

        # Assert that the login fails with 400 Bad Request or 401 Unauthorized
        assert (
            response.status_code == 401
        )  # Assuming 401 Unauthorized for incorrect credentials

    def test_login_non_existent_user(self):
        # Non-existent email
        data = {"username": "nonexistent", "password": "password123"}

        # Send POST request to the login endpoint
        response = self.client.post(self.url, data)

        # Assert that the login fails with 400 Bad Request or 401 Unauthorized
        assert (
            response.status_code == 401
        )  # Assuming 401 Unauthorized for non-existent user
