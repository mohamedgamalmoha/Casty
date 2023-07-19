from .models import User
from .enums import RoleChoices


def is_non_admin_user(user: User) -> bool:
    """Check whether the user it admin or not. Return True in case of being a non admin."""
    return user.role != RoleChoices.ADMIN
