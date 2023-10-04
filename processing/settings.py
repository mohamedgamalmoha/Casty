import copy
from collections import namedtuple

from django.conf import settings

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


def get_settings():
    defaults = copy.deepcopy(DEFAULTS)
    if hasattr(settings, SETTING_NAME):
        defaults.update(getattr(settings, SETTING_NAME))

    _settings = {}
    for key, val in defaults.items():
        if requires_import(key):
            val = perform_import(val, key)
        _settings[key] = val

    Setting = namedtuple("Data", _settings.keys())
    return Setting(**_settings)


processing_settings = get_settings()
