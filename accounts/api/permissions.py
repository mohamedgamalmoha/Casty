from rest_framework.permissions import BasePermission, SAFE_METHODS

from agencies.models import Agency
from profiles.models import Profile
from accounts.utils import is_non_admin_user, is_model_user, is_director_model


class ReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS


class IsModelUser(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_model_user(user)

    def has_object_permission(self, request, view, obj) -> bool:
        if isinstance(obj, Profile):
            return obj.user == request.user
        profile = getattr(obj, 'profile', None)
        if isinstance(profile, Profile):
            return profile.user == request.user
        return False


class IsDirectorUser(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_director_model(user)

    def has_object_permission(self, request, view, obj) -> bool:
        if isinstance(obj, Agency):
            return obj.user == request.user
        profile = getattr(obj, 'agency', None)
        if isinstance(profile, Agency):
            return profile.user == request.user
        return False


class DenyDelete(BasePermission):

    def has_permission(self, request, view) -> bool:
        return not request.method == 'DELETE'


class IsAuthenticatedNoneAdmin(BasePermission):

    def has_permission(self, request, view) -> bool:
        user = request.user
        return user.is_authenticated and is_non_admin_user(user)
