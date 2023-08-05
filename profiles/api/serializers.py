from django.contrib.auth.backends import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from profiles.enums import GenderChoices
from profiles.models import Skill, Language, Profile, SocialLink, PreviousExperience, ProfileImage


User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        exclude = ()
        read_only_fields = ('id', 'name', 'is_active', 'create_at', 'update_at')


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        exclude = ()
        read_only_fields = ('id', 'name', 'code', 'create_at', 'update_at')


class SocialLinkSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(read_only=True)

    class Meta:
        model = SocialLink
        exclude = ()
        read_only_fields = ('id', 'profile', 'domain', 'create_at', 'update_at')


class PreviousExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreviousExperience
        exclude = ()
        read_only_fields = ('id', 'profile', 'create_at', 'update_at')


class ProfileSerializer(FlexFieldsModelSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        exclude = ('following_models', 'following_agencies')
        read_only_fields = ('id', 'user', 'model_class', 'create_at', 'update_at', 'age')
        expandable_fields = {
            'user': ('accounts.api.serializers.CustomUserSerializer', {'many': False, 'read_only': True,
                                                                       'omit': ['profile']}),
            'links': ('profiles.api.serializers.SocialLinkSerializer', {'many': True, 'read_only': True}),
            'experiences': ('profiles.api.serializers.PreviousExperienceSerializer', {'many': True, 'read_only': True}),
            'images':  ('profiles.api.serializers.ProfileImageSerializer', {'many': True, 'read_only': True})
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Set default image based on gender
        if not instance.image:
            if instance.gender == GenderChoices.FEMALE:
                data['image'] = '/static/images/profile_female.png'
            else:
                data['image'] = '/static/images/profile_male.png'

        # Set default cover in case of being empty
        if not instance.cover:
            data['cover'] = '/static/images/profile_cover.jpg'

        return data


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        exclude = ()
        read_only_fields = ('id', 'profile', 'create_at', 'update_at')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            if ProfileImage.objects.filter(profile=request.user.profile).count() >= ProfileImage.MAXIMUM_NUMBER:
                raise serializers.ValidationError(
                    _('You have reached the maximum number of images that could be created')
                )
        return attrs
