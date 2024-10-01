from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..serializers.events import (
    EventSerializer,
    EventSectionSerializer,
)

from ..permissions import (
    IsHostingUserPermission,
    OwnerEventPermissions,
)
from ..models import Event
from drf_spectacular.utils import extend_schema


# Create your views here.
@extend_schema(tags=["Events"])
class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# Create your views here.
@extend_schema(tags=["Events"])
class EventCreateAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsHostingUserPermission]


# Detail for events
@extend_schema(tags=["Events"])
class EventRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSectionSerializer
    lookup_field = "pk"


# update Events Sections
@extend_schema(tags=["Events"])
class EventUpdateAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [
        IsAuthenticated,
        OwnerEventPermissions,
    ]
