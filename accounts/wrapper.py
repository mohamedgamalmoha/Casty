from django.conf import settings

from .tasks import process_context_with_request, send_mail


class EmailWrapper:

    def __init__(self, request, context, url_name=None):
        self.request = request
        self.context = context
        self.url_name = url_name

    def send(self, to):
        self.to = to
        context = process_context_with_request(self.context, self.request, self.url_name)
        if getattr(settings, 'CELERY_EMAIL_USE', True):
            send_mail.delay(context, self.to)
        else:
            send_mail(context, self.to)
