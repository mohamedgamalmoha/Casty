from typing import Dict
from django.apps import apps
from django.db import models
from django.http.request import HttpRequest
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.request import Request as DRFRequest


def encode_http_request(request) -> Dict[str, str]:
    site = get_current_site(request)
    return {
        'domain': site.domain,
        'site_name': site.name,
        'protocol': 'https' if request.is_secure() else 'http',
        # Custom key which used to get the target email class handler
        'url_name': request.resolver_match.url_name
    }


def decode_http_request(request: dict):
    return request


def encode_model_instance(obj: models.Model):
    return {
        'pk': obj.pk,
        # Meta tag data is used to reverse this instance, convert from dict to model instance.
        # Ignoring those will lead to serious problem.
        'meta': {
            'app_label': obj._meta.app_label,  # app_label: The name of the app the model belongs to.
            'model_name': obj._meta.model_name,  # model_name: The name of the model (usually in lowercase).
            'object_name': obj._meta.object_name  # object_name: The actual name of the model class.
        }
    }


def decode_model_instance(obj_dict: dict):
    try:
        app_label, object_name = obj_dict['meta']['app_label'], obj_dict['meta']['object_name']
        Class = apps.get_model(app_label, object_name)
        return Class.objects.get(pk=obj_dict['pk'])
    except (LookupError, models.ObjectDoesNotExist):
        return obj_dict


CELERY_TYPES = (
    (models.Model, "model", encode_model_instance, decode_model_instance),
    (HttpRequest, "request", encode_http_request, decode_http_request),
    (DRFRequest, "request", encode_http_request, decode_http_request),
)
