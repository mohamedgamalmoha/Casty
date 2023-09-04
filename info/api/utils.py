from typing import Set, Tuple

from django.db import models
from django.utils import translation


def is_translatable_field(field: models.Field) -> bool:
    """
    Check if a Django model field is marked for translation.

    This function determines whether a given Django model field is marked for translation by
    checking if it has an attribute named 'translated_field'. Fields marked for translation can
    have their values translated into multiple languages.

    Args:
    - field (models.Field): The Django model field to check.

    Returns:
        bool: True if the field is marked for translation (has 'translated_field' attribute), False
        otherwise.
    """
    return hasattr(field, 'translated_field')


def is_excluded_field(field_name: str) -> bool:
    """
    Check if a field name should be excluded based on the current language.

    This function determines whether a field name should be excluded from the queryset based on
    the current language. It checks if the field name ends with the current language code, and
    if it doesn't, it indicates that the field should be excluded. This can be useful when
    filtering out language-specific fields in a multi-language application.

    Args:
        - field_name (str): The name of the field to check for exclusion.

    Returns:
        bool: True if the field should be excluded based on the current language, False otherwise.
    """
    curr_lang = translation.get_language()
    return not field_name.endswith(f'_{curr_lang}')


def get_translatable_model_fields(model: models.Model) -> Set[Tuple[str, models.Field]]:
    """
    Get a set of fields from a Django model that are marked for translation.

    This function retrieves a set of fields from a Django model that are marked for translation
    by checking if they have an attribute named 'translated_field'. Fields marked for translation
    can have their values translated into multiple languages.

    Args:
        - model (models.Model): The Django model for which to retrieve translatable fields.

    Returns:
        Set[Tuple[str, models.Field]]: A set of tuples containing field names and corresponding field instances that
        are marked for translation in the provided model.
    """
    return set(filter(lambda field: is_translatable_field(field), model. _meta.get_fields()))
