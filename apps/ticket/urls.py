from django.urls import path
from . import views


app_name = "tickets-app"


urlpatterns = [
    # Host User Event (Authenticated)
    path(
        "event/<int:event_id>/ticket/create/",
        views.EventCreateTicketAPIView.as_view(),
        name="event-ticket-create",
    ),
    path(
        "event/<slug:slug>/ticket/buyer/",
        views.TicketSellerBuyerAPIView.as_view(),
        name="event-ticket-buyer",
    ),
    path(
        "event/<int:event_id>/detail/",
        views.TicketRetrieveAPIView.as_view(),
        name="event-detail",
    ),
    # for Normal User (Not Authenticate)
    path(
        "event/<int:event_id>/",
        views.EventTicketAPIView.as_view(),
        name="event-ticket",
    ),
]
