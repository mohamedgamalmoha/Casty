from rest_framework import serializers

from info.models import (MainInfo, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, FAQs, ContactUs, HeaderImage,
                         TeamMember)
from .mixins import TranslationModelSerializerMixin


class MainInfoSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = MainInfo
        exclude = ()


class AboutUsSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        exclude = ()


class TermsOfServiceSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = TermsOfService
        exclude = ()


class CookiePolicySerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = CookiePolicy
        exclude = ()


class PrivacyPolicySerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = PrivacyPolicy
        exclude = ()


class FAQsSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = FAQs
        exclude = ()


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        exclude = ('create_at', 'update_at')


class HeaderImageSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = HeaderImage
        exclude = ()


class TeamMemberSerializer(TranslationModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = TeamMember
        exclude = ()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context['request']

        # Set default image in case of being none
        if not instance.image:
            data['image'] = request.build_absolute_uri('/static/images/profile_male.png')

        return data
