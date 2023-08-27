from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.utils import is_non_admin_user, is_model_user, is_director_user, is_owner


class ReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS


class IsModelUser(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_model_user(user)

    def has_object_permission(self, request, view, obj) -> bool:
        return is_owner(request.user, obj)


class IsDirectorUser(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_director_user(user)

    def has_object_permission(self, request, view, obj) -> bool:
        return is_owner(request.user, obj)


class DenyDelete(BasePermission):

    def has_permission(self, request, view) -> bool:
        return not request.method == 'DELETE'


class IsAuthenticatedNoneAdmin(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_non_admin_user(user)
