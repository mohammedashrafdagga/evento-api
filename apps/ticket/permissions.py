from rest_framework.permissions import BasePermission


class OwnerEventTicketPermission(BasePermission):
    message = "Tickets Can See By Owner of this Event Only"

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.event.host == user


class OwnerEventPermission(BasePermission):
    message = "Tickets Can See Or Create By Owner of this Event Only"

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.host == user
