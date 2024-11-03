from faker import Faker

from .base import *

faker = Faker()


class TestEvent(BaseTest):
    def test_get_events(self):
        response = self.client.get(reverse("event-app:list"))
        assert response.status_code == 200
        assert len(response.data) == 1

    # test create event
    def test_create_event_for_non_authorize(self):
        response = self.client.post(
            reverse("event-app:create"),
            data={
                "host": self.user,
                "name": faker.catch_phrase(),
                "description": faker.paragraph(),
                "start_date": faker.date_time_this_year(),
                "end_date": faker.date_time_this_year(),
                "location": faker.address(),
                "category": self.category,
                "availability": random.choice(["all", "specific"]),
            },
        )
        # unauthorized
        assert response.status_code == 401

    # test create event
    def test_create_event_for_authorize(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user_auth)
        response = self.client.post(
            reverse("event-app:create"),
            {
                "host": self.user,
                "name": faker.catch_phrase(),
                "description": faker.paragraph(),
                "start_date": faker.date_this_year(),
                "end_date": faker.date_this_year(),
                "location": faker.address(),
                "category": self.category,
                "availability": random.choice(["all", "specific"]),
            },
        )

        # unauthorized
        assert response.status_code == 201
