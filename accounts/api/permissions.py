from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.utils import is_non_admin_user


class ReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS


class IsUserWithProfile(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and hasattr(request.user, 'profile')


class DenyDelete(BasePermission):

    def has_permission(self, request, view) -> bool:
        return not request.method == 'DELETE'


class IsAuthenticatedNoneAdmin(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_non_admin_user(user)
