from django.urls import path
from .views.event import (
    EventListAPIView,
    EventCreateAPIView,
    EventRetrieveAPIView,
    EventUpdateAPIView,
    JoinEventAPIView,
    AcceptUserAPIView,
)
from .views.category import CategoryListAPIView, CategoryDetailAPIView
from .views.section import (
    SectionCreateAPIView,
    SectionDetailAPIView,
    SectionUpdateAPIView,
    SectionDestroyAPIView,
)


app_name = "event-app"

urlpatterns = [
    path("", EventListAPIView.as_view(), name="list"),
    path("create/", EventCreateAPIView.as_view(), name="create"),
    path("join/<int:pk>/", JoinEventAPIView.as_view(), name="join_event"),
    # For Hosting User for Event
    path("accepted/", AcceptUserAPIView.as_view(), name="accept_user"),
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path(
        "categories/<slug:slug>/",
        CategoryDetailAPIView.as_view(),
        name="category-detail",
    ),
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
    path("<int:pk>/", EventRetrieveAPIView.as_view(), name="detail"),
    path("<int:pk>/update/", EventUpdateAPIView.as_view(), name="update"),
]
