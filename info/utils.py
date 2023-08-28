from typing import List

from django.utils.safestring import mark_safe


def get_model_fields_names(instance, exclude: List[str] = None) -> List[str]:
    """Get fields names from model instance."""
    # init exclude parameter as lis in case of bing none
    if exclude is None:
        exclude = []
    return list(filter(
        lambda field_name: field_name not in exclude,  # ignore field in cas of bing at exclude list
        map(lambda field: field.name, instance._meta.get_fields())  # get fields names as str
    ))


def create_html_icon_link(link: str, icon: str) -> str:
    """Create html link with icon for a given link"""
    return mark_safe(f"""<a href="{link}" title="{icon} link"><i class="fab fa-{icon}"></i></a>""")
