from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from api.models import Product


class ProfileEditIfIsOwner(permissions.BasePermission):
    edit_methods = ('PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in self.edit_methods and obj.id == request.user.username:
            return True

        if request.method == 'GET':
            return True

        return False


class ProductEditIfIsOwner(permissions.BasePermission):
    edit_methods = ('PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in self.edit_methods and obj.owner.id == request.user.username:
            return True

        if request.method == 'GET':
            return True

        return False


class ProductImageEditIfIsOwner(permissions.BasePermission):
    edit_methods = ('POST', 'DELETE')

    def has_permission(self, request, view):
        product = get_object_or_404(Product, id=view.kwargs.get('pk'))
        return product.owner_id == request.user.username

    def has_object_permission(self, request, view, obj):
        return True


class ProfileRentsIfIsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        renter_id = view.kwargs.get('pk')
        return request.user.is_authenticated and renter_id == request.user.username

    def has_object_permission(self, request, view, obj):
        return True


# Only owner can set to accepted or rejected, only renter can set to canceled
class RentPatchIfIsOwnerOrRenter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if obj.product.owner.id == request.user.username:
            if request.data.get('status') not in ['accepted', 'rejected']:
                return False
            return True

        if obj.renter.id == request.user.username:
            if request.data.get('status') != 'canceled':
                return False
            return True

        if request.method == 'GET':
            return False

        return False


class RentDeleteIfIsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if obj.product.owner.id == request.user.username:
            return True

        return False
