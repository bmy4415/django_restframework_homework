from rest_framework import permissions


class IsRelated(permissions.BasePermission):
    """
    Custom permission to only allow users that related to promise.
    """

    def has_object_permission(self, request, view, obj):
        # if not related, false
        if request.user.id not in [obj.user1.id, obj.user2.id]:
            return False

        return True
