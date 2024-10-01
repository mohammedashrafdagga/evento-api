from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from ..serializers.events import (
    EventSerializer,
    EventSectionSerializer,
    AcceptUserSerializer,
)

from ..permissions import (
    IsHostingUserPermission,
    OwnerEventPermissions,
)
from ..models import Event
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ..utils.user_join_event import UserJoinEventServices


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


# Allow to User Join Event as Participant
@extend_schema(tags=["Events"])
class JoinEventAPIView(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        event = self.get_object()
        user = request.user

        # check User Join
        UserJoinEventServices.check_user_already_join(event=event, user=user)
        UserJoinEventServices.check_user_not_host_event(event, user)
        message = UserJoinEventServices.add_user_to_event(event, user)

        return Response(
            {"detail": message},
            status=status.HTTP_200_OK,
        )


# AcceptUserAPIView
@extend_schema(tags=["Events"])
class AcceptUserAPIView(generics.GenericAPIView):
    """we edit That Accept Event Scenario"""

    serializer_class = AcceptUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = AcceptUserSerializer(data=request.data)
        if serializer.is_valid():
            UserJoinEventServices.check_user_host_event(
                event=Event.objects.get(id=serializer.validated_data["event_id"]),
                user=request.user,
            )
            UserJoinEventServices.accept_user(
                user_id=serializer.validated_data["user_id"],
                event_id=serializer.validated_data["event_id"],
            )
            # send notification for User
            return Response(
                {"detail": "You have been accepted to the event."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
