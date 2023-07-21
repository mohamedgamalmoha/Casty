from django.contrib.auth.backends import get_user_model

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from agencies.models import Agency, PreviousWork


User = get_user_model()


class PreviousWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreviousWork
        exclude = ()
        read_only_fields = ('id', 'create_at', 'update_at')


class AgencySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Agency
        exclude = ()
        read_only_fields = ('id', 'user', 'is_authorized', 'create_at', 'update_at')
        expandable_fields = {
            'works': (PreviousWorkSerializer, {'many': True, 'read_only': True}),
        }
