from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from reviews.models import Rate
from contracts.models import ContractRequest, SoloContract
from reports.api.utils import get_object_or_none
from reports.api.serializers import ContentObjectRelatedField


MODELS_MAP = {
    'contract-request': ContractRequest,
    'solo-contract': SoloContract
}


class RateSerializer(FlexFieldsModelSerializer):
    content_object = ContentObjectRelatedField(models_map=MODELS_MAP, read_only=True)

    class Meta:
        model = Rate
        read_only_fields = ('id', 'agency', 'profile', 'content_object', 'create_at', 'update_at')
        exclude = ('content_type', 'object_id')
        expandable_fields = {
            'agency': ('agencies.api.serializers.AgencySerializer', {'many': False, 'read_only': True}),
            'profile': ('profiles.api.serializers.ProfileSerializer', {'many': False, 'read_only': True})
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
            name = model.__name__
            raise serializers.ValidationError(
                _(f'No instance of {name} model matches the target id {pk}.')
            )

        # Check if the user reports a model that his own
        user = request.user
        if (isinstance(obj, ContractRequest) and obj.contract.agency != user.aggency) or \
                (isinstance(obj, SoloContract) and obj.agency != user.aggency):
            name = model.__name__
            raise serializers.ValidationError(
                _(f'Director can`t review a model {name} that he doest have a deal with.')
            )

        # Check it the profiles are matched
        if obj.profile != data.profile:
            raise serializers.ValidationError(
                _(f'Profiles are not matched')
            )

        # Set content object to be saved in create function
        self.content_object = obj
        return data

    def create(self, validated_data):
        content_object = getattr(self, 'content_object', None)
        if content_object is not None:
            validated_data.update({'content_object': content_object})
        return super().create(validated_data)
