from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            username = obj.user.username
        except AttributeError:
            username = obj.username
        if request.method in permissions.SAFE_METHODS:
            return True
        return username == request.user.username
