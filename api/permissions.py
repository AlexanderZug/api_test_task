from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        print(request.user)
        # for i in obj:
        #     print(i)
        print(obj.username)
        return (obj.username == request.user
                or request.method in permissions.SAFE_METHODS)
