from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsHostingUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "hosting"


# Owner Event Permissions
class OwnerEventPermissions(BasePermission):
    def has_permission(self, request, view):
        event_id = request.data.get("event") or view.kwargs.get("event")

        if not event_id:
            # If no event_id is provided, deny permission
            raise PermissionDenied("No event ID provided in the request.")

        # Try to fetch the event object using the event_id
        from .models import Event  # Import the Event model

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            # If the event does not exist, deny permission
            raise PermissionDenied("The event does not exist.")

        # Check if the user is the host of the event
        if event.host != request.user:
            raise PermissionDenied(
                "You do not have permission to modify this event. You must be the host of the event."
            )

        return True
