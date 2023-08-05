from django.core.serializers import serialize
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from accounts.utils import is_owner
from reports.models import Report, ReportResponse
from agencies.models import Agency, PreviousWork, AgencyImage
from profiles.models import Profile, SocialLink, PreviousExperience, ProfileImage
from .utils import get_object_or_none


MODELS_MAP = {
    'profile': Profile,
    'social-link': SocialLink,
    'previous-experience': PreviousExperience,
    'profile-image': ProfileImage,
    'agency': Agency,
    'previous-work': PreviousWork,
    'agency-image': AgencyImage,
}


class ContentObjectRelatedField(serializers.RelatedField):

    def __init__(self, models_map: dict, **kwargs):
        self.models_map = models_map
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        action = self.context['action']
        pk = self.context['pk']
        model = self.models_map.get(action)
        return get_object_or_none(model, pk=pk)

    def to_representation(self, obj):
        try:
            Serializer = import_string(
                f'{obj._meta.app_label}.api.serializers.{obj._meta.object_name}Serializer'
            )
            return Serializer(obj).data
        except (ImportError, ValueError):
            return serialize('json', [obj])


class ReportSerializer(FlexFieldsModelSerializer):
    content_object = ContentObjectRelatedField(models_map=MODELS_MAP, read_only=True)

    class Meta:
        model = Report
        read_only_fields = ('id', 'user', 'content_object', 'create_at', 'update_at')
        exclude = ('content_type', 'object_id')
        expandable_fields = {
            'responses': ('reports.api.serializers.ReportResponseSerializer', {'many': False, 'read_only': True})
        }

    def validate(self, data):
        # Ignore in case of being POST request
        request = self.context['request']
        if request.method != 'POST':
            return data

        # Get action & pk from view
        action = self.context['action']
        pk = self.context['pk']

        # Check if the model is not matching
        model = MODELS_MAP.get(action, None)
        if model is None:
            raise serializers.ValidationError(
                _('Invalid Action.')
            )

        # Check if the pk matches the model or not
        obj = get_object_or_none(model, pk=pk)
        if obj is None:
            raise serializers.ValidationError(
                _(f'No instance of {model.__name__} model matches the target id {pk}.')
            )

        # Check if the user reports a model that his own
        user = request.user
        if is_owner(user, obj):
            raise serializers.ValidationError(
                _(f'User can`t report a model {model.__name__} that he owns.')
            )

        # Set content object to be saved in create function
        self.content_object = obj
        return data

    def create(self, validated_data):
        content_object = getattr(self, 'content_object', None)
        if content_object is not None:
            validated_data.update({'content_object': content_object})
        return super(ReportSerializer, self).create(validated_data)


class ReportResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportResponse
        exclude = ()
        read_only_fields = ('id', 'user', 'create_at', 'update_at')

    def validate(self, data):
        # Ignore in case of being POST request
        request = self.context['request']
        if request.method != 'POST':
            return data

        # Check if the user own the report
        if not is_owner(request.user, data['report']):
            raise serializers.ValidationError(
                _('User can\'t create a response for report that he doesn\'t own')
            )

        return data

    def update(self, instance, validated_data):
        # Exclude the report field from validated_data
        if 'report' in validated_data:
            validated_data.pop('report')
        return super().update(instance, validated_data)
