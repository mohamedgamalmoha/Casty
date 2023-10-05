from celery import shared_task
from celery.utils.log import get_task_logger

from .email import URL_EMAIL_MAP


logger = get_task_logger(__name__)


# autoretry_for: If any exceptions from the list/tuple occurs during task execution, the task will be automatically retried.
# retry_backoff: autoretries will be delayed following the rules of exponential backoff.
# max_retries: Maximum number of retries before giving up.
# The first retry will have a delay of 2 sec, the second is 4 sec, the third is 8 sec, the fourth is 16 sec, and so on ...
@shared_task(autoretry_for=(Exception,), max_retries=5, retry_backoff=2)
def send_mail(request, context, to, email_map_name):
    EmailClass = URL_EMAIL_MAP[email_map_name]
    EmailClass(request=request, context=context).send(to)
    logger.info("Email sent successfully. [To: %s, Url: %s]", to, email_map_name)
