from django.conf import settings

from .tasks import process_context_with_request, send_mail


class EmailWrapper:

    def __init__(self, request, context):
        self.request = request
        self.context = context

    def send(self, to):
        self.to = to
        context = process_context_with_request(self.context, self.request)
        if getattr(settings, 'CELERY_EMAIL_USE', True):
            send_mail.delay(context, self.to)
        else:
            send_mail(context, self.to)
