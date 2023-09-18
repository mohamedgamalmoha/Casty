from collections import namedtuple

from django.apps import apps
from django.db import models
from django.conf import settings
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from celery import shared_task

from .email import URL_EMAIL_MAP


User = get_user_model()


def model_to_dict_with_meta(obj):
    obj_dict = model_to_dict(obj, fields=['id'])
    obj_dict['pk'] = obj_dict['id']
    # Meta tag data is used to reverse this instance, convert from dict to model instance.
    # Ignoring those will lead to serious problem.
    obj_dict['meta'] = {
        'app_label': obj._meta.app_label,  # app_label: The name of the app the model belongs to.
        'model_name': obj._meta.model_name,  # model_name: The name of the model (usually in lowercase).
        'object_name': obj._meta.object_name   # object_name: The actual name of the model class.
    }
    return obj_dict


def dict_to_model(dct):
    try:
        app_label, object_name = dct['meta']['app_label'], dct['meta']['object_name']
        Class = apps.get_model(app_label, object_name)
        return Class.objects.get(id=dct['id'])
    except LookupError or models.ObjectDoesNotExist:
        # Define the named tuple based on the dictionary's keys
        Data = namedtuple("Data", dct.keys())
        # Convert the dictionary to the named tuple
        return Data(**dct)


def is_model_dict(dct):
    if not isinstance(dct, dict):
        return False
    meta = dct.get('meta', None)
    if not meta or not isinstance(meta, dict):
        return False
    return meta.get('app_label', None) and meta.get('object_name', None)


def process_context_with_request(context, request):
    con = context.copy()

    # Convert each model instance to dictionary
    for key, value in con.items():
        if isinstance(value, models.Model):
            con[key] = model_to_dict_with_meta(value)

    # Get site info from request, necessary step to show the link in the right format
    # Request object can not be serialized
    site = get_current_site(request)
    con.update({
        'domain': site.domain,
        'site_name': site.name,
        'protocol': 'https' if request.is_secure() else 'http'
    })

    # Set url name from request, it is used to get the target email class
    con['url_name'] = request.resolver_match.url_name
    return con


def process_context(context):
    # Convert each model dictionary to model instance
    for key, value in context.items():
        if is_model_dict(value):
            context[key] = dict_to_model(value)
    return context


@shared_task()
def send_mail(context, to):
    context = process_context(context)
    EmailClass = URL_EMAIL_MAP[context['url_name']]
    EmailClass(context=context).send(to)


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
