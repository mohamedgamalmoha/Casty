from typing import Type, Union

from django.db import models

from agencies.models import Agency
from profiles.models import Profile
from contracts.models import ContractRequest
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


def get_owner(obj: Type[models.Model]) -> bool:
    """Get the owner user of the object"""
    if hasattr(obj, 'user'):
        return obj.user
    if hasattr(obj, 'profile') and isinstance(obj.profile, Profile) and obj.profile is not None:
        return obj.profile.user
    if hasattr(obj, 'agency') and isinstance(obj.agency, Agency) and obj.agency is not None:
        return obj.agency
    if isinstance(obj, ContractRequest) and obj.contract is not None:
        return obj.contract.agency.user


def is_owner(user: User, obj: Type[models.Model]) -> bool:
    """Check whether the user is the owner of the object"""
    return get_owner(obj) == user


def get_user_associated_model(user: User) -> Union[Profile, Agency, None]:
    """Get the associated model (Profile or Agency or None) for a user."""
    if is_model_user(user):
        return getattr(user, 'profile')
    if is_director_user(user):
        return getattr(user, 'agency')
    return None
