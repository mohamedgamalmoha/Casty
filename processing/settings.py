from django.conf import settings
from django.test.signals import setting_changed

from rest_framework.settings import perform_import


SETTING_NAME = 'PROFESSING'

DEFAULTS = {
    'MODELS_WITH_IMAGE': (
        'profiles.models.Profile',
        'profiles.models.ProfileImage',
        'agencies.models.AgencyImage',
        'reports.models.Report'
    ),
    'GOOGLE_APPLICATION_CREDENTIALS': None,
    'IMAGE_FILED_NAME': 'image',
    'URL_NAME': 'default'
}

IMPORT_STRINGS = (
    'MODELS_WITH_IMAGE',
)


def requires_import(setting) -> bool:
    return setting in IMPORT_STRINGS


def load_settings():
    if hasattr(settings, SETTING_NAME):
        DEFAULTS.update(getattr(settings, SETTING_NAME))

    processing_settings = {}
    for key, val in DEFAULTS.items():
        if requires_import(key):
            val = perform_import(val, key)
        processing_settings[key] = val

    setattr(settings, SETTING_NAME, processing_settings)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == SETTING_NAME:
        load_settings()


setting_changed.connect(reload_api_settings)
