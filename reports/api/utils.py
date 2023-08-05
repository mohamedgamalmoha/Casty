from typing import Optional, Type, Dict, Any

from django.db import models


def get_object_or_none(model: Type[models.Model], **kwargs: Dict[str, Any]) -> Optional[models.Model]:
    """Gets an object from the database, or returns `None` if the object does not exist."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
