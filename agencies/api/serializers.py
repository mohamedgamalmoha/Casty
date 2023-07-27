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
    following_models_count = serializers.SerializerMethodField()
    followers_models_count = serializers.SerializerMethodField()
    following_agencies_count = serializers.SerializerMethodField()
    followers_agencies_count = serializers.SerializerMethodField()

    class Meta:
        model = Agency
        exclude = ()
        read_only_fields = ('id', 'user', 'following_models', 'following_agencies', 'is_authorized', 'create_at',
                            'update_at', 'following_models_count', 'followers_models_count', 'following_agencies_count',
                            'followers_agencies_count')
        expandable_fields = {
            'works': (PreviousWorkSerializer, {'many': True, 'read_only': True}),
            'following_models': ('profiles.api.serializers.ProfileSerializer', {'many': True, 'read_only': True}),
            'following_agencies': ('agencies.api.serializers.AgencySerializer', {'many': True, 'read_only': True}),
        }

    def get_following_models_count(self, instance) -> int:
        return instance.following_models.count()

    def get_followers_models_count(self, instance) -> int:
        return instance.follower_models.count()

    def get_following_agencies_count(self, instance) -> int:
        return instance.following_agencies.count()

    def get_followers_agencies_count(self, instance) -> int:
        return instance.follower_agencies.count()
