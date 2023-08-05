from django.contrib.auth.backends import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from agencies.models import Agency, PreviousWork, AgencyImage


User = get_user_model()


class PreviousWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreviousWork
        exclude = ()
        read_only_fields = ('id', 'create_at', 'update_at')


class AgencySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Agency
        exclude = ('following_models', 'following_agencies')
        read_only_fields = ('id', 'user', 'is_authorized', 'create_at', 'update_at')
        expandable_fields = {
            'works': (PreviousWorkSerializer, {'many': True, 'read_only': True}),
        }


class AgencyImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgencyImage
        exclude = ()
        read_only_fields = ('id', 'profile', 'create_at', 'update_at')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            if AgencyImage.objects.filter(profile=request.user.agency).count() >= AgencyImage.MAXIMUM_NUMBER:
                raise serializers.ValidationError(
                    _('You have reached the maximum number of images that could be created')
                )
        return attrs
