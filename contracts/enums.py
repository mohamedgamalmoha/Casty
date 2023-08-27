from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.IntegerChoices):
    PENDING = 0, _('Pending')
    ACCEPTED = 1, _('Accepted')
    REJECTED = 3, _('Rejected')
    OTHER = 4, _('Other')
