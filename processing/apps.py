from django.apps import AppConfig


class ProcessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'processing'

    def ready(self):
        from .checks import google_credentials_json_file_check
        from .signals import connect_image_detect_signals_to_models

        google_credentials_json_file_check()
        connect_image_detect_signals_to_models()
