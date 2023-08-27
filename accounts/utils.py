from typing import Type, Union

from django.db import models

from agencies.models import Agency
from profiles.models import Profile
from .models import User
from .enums import RoleChoices


def _is_user_with_role(user: User, role: int) -> bool:
    """Check whether the user has the target role."""
    return getattr(user, 'role', None) == role


def _is_instance_user(user: User, model: models.Model) -> bool:
    """Check whether the user has the target type of profile."""
    return isinstance(getattr(user, model.__name__.lower(), None), model)


def is_admin_user(user: User) -> bool:
    """Check whether the user is admin."""
    return _is_user_with_role(user, RoleChoices.ADMIN)


def is_non_admin_user(user: User) -> bool:
    """Check whether the user is not admin."""
    return not is_admin_user(user)


def is_model_user(user: User) -> bool:
    """Check whether the user has an instance of profile and match the type."""
    return _is_instance_user(user, Profile) and _is_user_with_role(user, RoleChoices.MODEL)


def is_director_user(user: User) -> bool:
    """Check whether the user has an instance of director and match the type."""
    return _is_instance_user(user, Agency) and _is_user_with_role(user, RoleChoices.DIRECTOR)


def is_owner(user: User, obj: Type[models.Model]) -> bool:
    """Check whether the user is the owner of the object"""
    if hasattr(obj, 'user'):
        if getattr(obj, 'user') == user:
            return True
    if is_model_user(user) and hasattr(obj, 'profile'):
        if getattr(obj, 'profile', None) == user.profile:
            return True
    if is_director_user(user) and hasattr(obj, 'agency'):
        if getattr(user, 'agency', None) == user.agency:
            return True
    return False


def get_user_associated_model(user: User) -> Union[Profile, Agency, None]:
    """Get the associated model (Profile or Agency or None) for a user."""
    if is_model_user(user):
        return getattr(user, 'profile')
    if is_director_user(user):
        return getattr(user, 'agency')
    return None
