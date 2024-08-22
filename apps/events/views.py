from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer, EventSectionSerializer, SectionSerializer
from .permissions import IsHostingUserPermission, OwnerEventPermissions
from .models import Event, Section
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


# Create your views here.
class EventCreateAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsHostingUserPermission]


# List Event API View
class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# Detail for events
class EventRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSectionSerializer
    lookup_field = "pk"


# update Events Sections
class EventUpdateAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsHostingUserPermission]


# Create Section
class SectionCreateAPIView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    # Want to Adding Another permission
    # Owner of Event
    permission_classes = [
        IsAuthenticated,
        IsHostingUserPermission,
        OwnerEventPermissions,
    ]


# Detail Event
class SectionDetailAPIView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]


# Update Section
class SectionUpdateAPIView(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [
        IsAuthenticated,
        IsHostingUserPermission,
        OwnerEventPermissions,
    ]


# Destroy Event
class SectionDestroyAPIView(SectionUpdateAPIView, generics.DestroyAPIView):
    pass


# Allow to User Join Event as Participant
class JoinEventView(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        event = self.get_object()
        user = request.user

        if event.participants.filter(id=user.id).exists():
            raise ValidationError("You have already joined this event.")

        if event.host == user:
            raise ValidationError("You cannot join an event that you are hosting.")

        event.participants.add(user)
        event.save()

        return Response(
            {"detail": "You have successfully joined the event."},
            status=status.HTTP_200_OK,
        )
