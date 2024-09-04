from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.exceptions import NotFound
from .permissions import OwnerNotificationPermissions
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .utils import NotificationService

# list notifications for user have
@extend_schema(tags=["Notifications"])
class UserNotificationListAPIView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-create_at"
        )


@extend_schema(tags=["Notifications"])
class MarkNotificationAsReadView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, OwnerNotificationPermissions]

    def patch(self, request, *args, **kwargs):
        try:
            notification = self.get_object()
        except Notification.DoesNotExist:
            raise NotFound("Notification Not Found")
        # make the notification is read
        NotificationService.read_notification(notification)

        return Response(
            {"detail": "Notification marked as read."}, status=status.HTTP_200_OK
        )
