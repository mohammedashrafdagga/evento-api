from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.exceptions import NotFound
from .permissions import OwnerNotificationPermissions
from rest_framework import status
from rest_framework.response import Response

# list notifications for user have
class UserNotificationListAPIView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-create_at"
        )


class MarkNotificationAsReadView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, OwnerNotificationPermissions]

    def patch(self, request, *args, **kwargs):
        try:
            notification = self.get_object()
        except Notification.DoesNotExist:
            raise NotFound("Notification Not Found")

        notification.status = Notification.NotificationStatus.READ
        notification.save()
        return Response(
            {"detail": "Notification marked as read."}, status=status.HTTP_200_OK
        )
