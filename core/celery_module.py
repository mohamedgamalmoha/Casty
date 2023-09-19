import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'update_rates': {
        'task': 'update_money_rates',
        'schedule': crontab(minute=0, hour=6),  # update rates every day at 6 am.
        'kwargs': {}
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
