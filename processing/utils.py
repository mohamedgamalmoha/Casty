from django.db import models


def get_image_fields(model):
    return [field.name for field in model._meta.fields if isinstance(field, models.ImageField)]
