import random

import pytest
from apps.events.models import *
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient

# initialize User Model and Faker
User = get_user_model()
faker = Faker()

# Base Test User
@pytest.mark.django_db
class BaseTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user",
            email="test_user@example.com",
            password="test_password",
            user_type="hosting",
            is_active=True,
        )

        self.category = Category.objects.create(name=faker.name())

        self.event = Event.objects.create(
            host=self.user,
            name=faker.catch_phrase(),
            description=faker.paragraph(),
            start_date=faker.date_time_this_year(),
            end_date=faker.date_time_this_year(),
            location=faker.address(),
            category=self.category,
            availability=random.choice(["all", "specific"]),
        )

        for _ in range(2):
            Section.objects.create(
                event=self.event,
                name=faker.catch_phrase(),
                description=faker.paragraph(),
                start_datetime=faker.date_time_this_year(),
                end_datetime=faker.date_time_this_year(),
                location=faker.address(),
                speaker=faker.name(),
            )

        # login User authentication
        login_response = self.client.post(
            reverse("auth-app:login"),
            data={"username": "test_user", "password": "test_password"},
        )
        self.user_auth = f"Bearer {login_response.data['access']}"
