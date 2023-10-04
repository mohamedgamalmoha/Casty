from django.conf import settings
from django.db.models import Model
from djoser.compat import get_user_email

from celery import shared_task
from celery.utils.log import get_task_logger

from accounts.utils import get_owner
from accounts.wrapper import EmailWrapper
from .settings import SETTING_NAME
from .google_utils import detect_explicit_image_content


logger = get_task_logger(__name__)
curr_settings = getattr(settings, SETTING_NAME)


@shared_task
def detect_model_image(instance: Model, image_field_name: str = curr_settings.IMAGE_FILED_NAME) -> None:
    from google.api_core.exceptions import PermissionDenied
    from google.auth.exceptions import DefaultCredentialsError

    try:
        image = getattr(instance, image_field_name)
        result = detect_explicit_image_content(image.path)
    except (DefaultCredentialsError, PermissionDenied):
        ...
    except Exception as exc:
        raise detect_model_image.retry(exc=exc, max_retries=3, retry_backoff=2)
    else:
        if result:
            user = get_owner(instance)
            context = {'user': user, 'messages': result}
            to = [get_user_email(user)]
            EmailWrapper(context=context, url_name=curr_settings.URL_NAME).send(to)
