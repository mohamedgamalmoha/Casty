from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleChoices(models.IntegerChoices):
    ADMIN = 0, _('Admin')
    MODEL = 1, _('Model')
    DIRECTOR = 2, _('Director')
    OTHER = 3, _('Other')

    @classmethod
    def excluded(cls, exclude: List = None):
        exclude = exclude or []
        return [(value, label) for value, label in cls.choices if value not in exclude]

    @classmethod
    def exclude_admin(cls):
        return cls.excluded([cls.ADMIN.value])


def get_role_label_from_value(value):
    RoleDict = dict(RoleChoices.choices)
    return RoleDict.get(value)
