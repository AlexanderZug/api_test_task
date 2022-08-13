from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.username == request.user
            or request.method in permissions.SAFE_METHODS
        )
