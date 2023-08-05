from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


def get_change_admin_url(model_instance):
    content_type = ContentType.objects.get_for_model(model_instance.__class__)
    admin_url = reverse("admin:{}_{}_change".format(content_type.app_label, content_type.model),
                        args=(model_instance.pk,))
    return admin_url
