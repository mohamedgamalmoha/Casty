from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from .enums import RoleChoices


class CustomUserManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        role = extra_fields.get('role', None)
        if role == RoleChoices.ADMIN:
            raise ValueError(
                _('Role shouldn\'t be null or equal to Admin')
            )
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', RoleChoices.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)

    def active(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_active=True)

    def exclude_admin(self, *args, **kwargs):
        return self.active().exclude(role=RoleChoices.ADMIN)


class User(AbstractUser):
    base_role = RoleChoices.OTHER

    email = models.EmailField(blank=False, unique=True, verbose_name=_('Email Address'))
    role = models.PositiveSmallIntegerField(choices=RoleChoices.choices, default=base_role, null=True,
                                            blank=True, verbose_name=_('Role'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email
