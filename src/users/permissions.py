from rest_framework import permissions


class ProfileEditIfIsOwner(permissions.BasePermission):
    edit_methods = ('PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in self.edit_methods and obj.id == request.user.username:
            return True

        if request.method == 'GET':
            return True

        return False
