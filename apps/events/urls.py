from django.urls import path
from .views import (
    EventCreateAPIView,
    EventListAPIView,
    EventRetrieveAPIView,
    EventUpdateAPIView,
    SectionCreateAPIView,
    SectionDetailAPIView,
    SectionUpdateAPIView,
    SectionDestroyAPIView,
    JoinEventView,
)


app_name = "event-app"

urlpatterns = [
    path("", EventListAPIView.as_view(), name="list"),
    path("create/", EventCreateAPIView.as_view(), name="create"),
    path("join/<int:pk>/", JoinEventView.as_view(), name="join_event"),
    path("<int:pk>/", EventRetrieveAPIView.as_view(), name="detail"),
    path("<int:pk>/update/", EventUpdateAPIView.as_view(), name="update"),
    path("sections/create/", SectionCreateAPIView.as_view(), name="section_create"),
    path("sections/<int:pk>/", SectionDetailAPIView.as_view(), name="section_detail"),
    path(
        "sections/<int:pk>/update/",
        SectionUpdateAPIView.as_view(),
        name="section_update",
    ),
    path(
        "sections/<int:pk>/delete/",
        SectionDestroyAPIView.as_view(),
        name="section_delete",
    ),
]
