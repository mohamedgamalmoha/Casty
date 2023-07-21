from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AgenciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agencies'
    verbose_name = _('Agencies')
