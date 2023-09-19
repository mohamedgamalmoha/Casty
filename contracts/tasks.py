from django.conf import settings
from django.utils.timezone import now
from django.utils.module_loading import import_string

from celery import current_app
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@current_app.task(name='update_money_rates', autoretry_for=(Exception,), max_retries=3, retry_backoff=60)
def update_money_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
    logger.info("Rate updated successfully. [Time: %s, Currency: %s]",  now(), ''.join(settings.CURRENCIES))
