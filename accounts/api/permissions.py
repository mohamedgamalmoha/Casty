from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.enums import RoleChoices
from accounts.utils import is_non_admin_user
from profiles.models import Profile


class ReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS


class IsUserWithProfile(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and user.role == RoleChoices.MODEL

    def has_object_permission(self, request, view, obj) -> bool:
        if isinstance(obj, Profile):
            return obj.user == request.user
        profile = getattr(obj, 'profile', None)
        if isinstance(profile, Profile):
            return profile.user == request.user
        return False


class DenyDelete(BasePermission):

    def has_permission(self, request, view) -> bool:
        return not request.method == 'DELETE'


class IsAuthenticatedNoneAdmin(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_non_admin_user(user)
