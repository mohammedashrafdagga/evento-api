from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsHostingUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "hosting"


# Owner Event Permissions
class OwnerEventPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "event"):
            if obj.event.host != request.user:
                raise PermissionDenied(
                    "You do not have permission to modify this section. You must be the host of the event."
                )

        elif obj.host == request.user:
            raise PermissionDenied(
                "You do not have permission to modify this event. You must be the host of the event."
            )
        return True
