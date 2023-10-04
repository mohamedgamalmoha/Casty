from django.conf import settings
from django.db.models.signals import pre_save, post_save

from .settings import SETTING_NAME
from .utils import get_image_fields
from .tasks import detect_model_image


curr_settings = getattr(settings, SETTING_NAME)


def image_detect_pre_save(sender, instance, created, **kwargs):
    if instance.id is not None:
        image_fields = get_image_fields(sender)
        previous = sender.objects.objects.get(id=instance.id)
        for image_field in image_fields:
            instance_image, previous_image = getattr(instance, image_field, None), getattr(previous, image_field, None)
            if instance_image is not None and previous_image is not None and instance_image != previous_image:
                detect_model_image.delay(instance_image)


def image_detect_post_save(sender, instance, created, **kwargs):
    if created:
        image_fields = get_image_fields(sender)
        for image_field in image_fields:
            instance_image = getattr(instance, image_field, None)
            if instance_image is not None:
                detect_model_image.delay(instance_image)


def connect_image_detect_signals_to_models():
    for model in curr_settings.MODELS_WITH_IMAGE:
        pre_save.connect(image_detect_pre_save, sender=model)
        post_save.connect(image_detect_post_save, sender=model)
