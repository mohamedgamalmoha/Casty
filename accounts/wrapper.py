from django.conf import settings
from kombu.utils.json import _encoders

from .tasks import send_mail


def get_json_decoder(obj):
    for t, (marker, encoder) in _encoders.items():
        if isinstance(obj, t):
            return encoder


def update_context_with_request(context, request):
    decoder = get_json_decoder(request)
    if decoder:
        context.update(decoder(request))


class EmailWrapper:

    def __init__(self, request, context, email_map_name=None):
        self.request = request
        self.context = context
        self.email_map_name = email_map_name

    def send(self, to):
        if self.email_map_name is None:
            self.email_map_name = self.get_email_map_name()
        if getattr(settings, 'CELERY_EMAIL_USE', True):
            update_context_with_request(self.context, self.request)
            send_mail.delay(None, self.context, to, self.email_map_name)
        else:
            send_mail(self.request, self.context, to, self.email_map_name)

    def get_email_map_name(self):
        email_map_name = self.context.get('email_map_name', None)
        if email_map_name is None and self.request is not None:
            return self.request.resolver_match.url_name
        return email_map_name
