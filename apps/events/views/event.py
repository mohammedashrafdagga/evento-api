from apps.events.models import Event
from apps.events.permissions import IsHostingUserPermission, OwnerEventPermissions
from apps.events.serializers.events import EventSectionSerializer, EventSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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
