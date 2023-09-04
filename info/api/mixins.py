from django.utils import translation
from rest_framework.permissions import SAFE_METHODS

from .utils import get_translatable_model_fields, is_excluded_field


class TranslationViewMixin:
    """
     A mixin for rest class-based views that provides functionality for handling translations.

     This mixin activates the appropriate language based on the 'Accept-Language' request header,
     and it excludes translatable fields from the queryset to prevent unnecessary database queries.

     Usage:
     - Inherit from this mixin in your Django class-based view.
     - Override the `get_queryset` method as needed.

     Attributes:
     - None

     Methods:
     - get_queryset(self): Returns a queryset with excluded translatable fields based on the
       'Accept-Language' header and the model's translatable fields configuration.

     Note:
     To use this mixin, make sure your Django project has properly configured translation settings,
     and the 'Accept-Language' header is correctly set in the request.

     Example:
         ```python
         class MyListView(TranslationViewMixin, ListView):
            model = MyModel
            # ... other view configuration ...
         ```
     """

    def get_queryset(self):
        """
        Override this method to customize the queryset for your view.

        Returns:
            queryset: A queryset with excluded translatable fields based on the 'Accept-Language' header.
        """

        # activate language in case of bing existed in request headers
        # the request header should be named as: Accept-Language
        if 'HTTP_ACCEPT_LANGUAGE' in self.request.META:
            lang = self.request.META['HTTP_ACCEPT_LANGUAGE']
            translation.activate(lang)

        queryset = super().get_queryset()

        # get translatable fields names from model in case of being excluded
        exclude_fields = set(
            field.name for field in get_translatable_model_fields(queryset.model)
            if is_excluded_field(field.name)
        )

        # exclude fields to not be fetched from database
        return queryset.defer(*exclude_fields)


class TranslationModelSerializerMixin:
    """
    A mixin for Django REST framework serializers that provides functionality for handling translations in serializers.

    This mixin customizes the serializer's fields based on the HTTP request method. When a safe
    (GET, HEAD, OPTIONS) request is made, it excludes translatable fields from the serialized
    output. This is useful when you want to reduce the amount of data transmitted in safe requests.

    Usage:
        - Inherit from this mixin in your Django REST framework serializer.
        - Override the `get_fields` method as needed.

    Attributes:
        - None

    Methods:
        - get_fields(self): Returns a dictionary of serializer fields, either with or without translatable fields,
        depending on the HTTP request method.

    Note:
        To use this mixin effectively, ensure that your Django project has properly configured translation settings
        and that your model's fields are correctly marked for translation.

    Example:
        ```python
        class MyModelSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):
            class Meta:
            model = MyModel
            fields = '__all__'
        ```
       """

    def get_fields(self):
        """
        Override this method to customize the serializer's fields.

        Returns:
            dict: A dictionary of serializer fields, with or without translatable fields based on the HTTP
            request method.
        """

        model = self.Meta.model
        fields = super().get_fields().items()

        # in case of the request method is not a safe one, return fields as they are
        if self.context['request'].method not in SAFE_METHODS:
            return fields

        # get translatable fields names from model
        translatable_fields_names = set(field.name for field in get_translatable_model_fields(model))

        # exclude translatable fields
        return {field_name: field for field_name, field in fields if field_name not in translatable_fields_names}
