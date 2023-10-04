from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProcessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'processing'
    verbose_name = _('Processing')

    def ready(self):
        # Add System checks
        from .checks import google_credentials_json_file_check  # NOQA
        from .signals import connect_image_detect_signals_to_models

        connect_image_detect_signals_to_models()
