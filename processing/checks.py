from django.conf import settings
from django.core.checks import Tags, Warning, register

from .settings import SETTING_NAME


curr_settings = getattr(settings, SETTING_NAME)


@register(Tags.compatibility)
def google_credentials_json_file_check(app_configs, **kwargs):
    errors = []
    if curr_settings.GOOGLE_APPLICATION_CREDENTIALS is None:
        errors.append(
            Warning(
                f"You have to specify a Google credentials json file path with key GOOGLE_APPLICATION_CREDENTIALS at "
                f"environment",
                hint="Specify the file path to be able to process image with google",
                id="processing.W001"
            )
        )
    return errors
