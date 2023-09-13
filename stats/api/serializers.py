from django.contrib.auth.backends import get_user_model

from rest_framework import serializers

from reviews.models import Rate
from reports.models import Report
from contracts.models import Contract, SoloContract
from reports.enums import get_type_label_from_value
from accounts.enums import get_role_label_from_value


User = get_user_model()


class BaseDateCountStatsSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    count = serializers.IntegerField()

    class Meta:
        fields = ('date', 'count')


class BaseLabelCountStatsSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    label = serializers.CharField()

    class Meta:
        fields = ('label', 'count')


class DateCountUserStatsSerializer(BaseDateCountStatsSerializer):

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = User


class RoleCountUserStatsSerializer(BaseLabelCountStatsSerializer):
    label = serializers.CharField(source='role')

    class Meta(BaseLabelCountStatsSerializer.Meta):
        model = User

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['label'] = get_role_label_from_value(int(representation['label']))
        return representation


class DateCountReportStatsSerializer(BaseDateCountStatsSerializer):

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = Report


class TypeCountReportStatsSerializer(BaseLabelCountStatsSerializer):
    label = serializers.CharField(source='type')

    class Meta(BaseLabelCountStatsSerializer.Meta):
        model = Report

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['label'] = get_type_label_from_value(int(representation['label']))
        return representation


class DateCountRateStatsSerializer(BaseDateCountStatsSerializer):

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = Rate


class RateCountRateStatsSerializer(BaseLabelCountStatsSerializer):
    label = serializers.CharField(source='rate')

    class Meta(BaseLabelCountStatsSerializer.Meta):
        model = Rate


class DateSumRateStatsSerializer(BaseDateCountStatsSerializer):
    sum = serializers.IntegerField()
    count = None

    class Meta:
        model = Rate
        fields = ('date', 'sum')


class DateCountContractStatsSerializer(BaseDateCountStatsSerializer):

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = Contract


class DateSumContractStatsSerializer(BaseDateCountStatsSerializer):
    sum = serializers.IntegerField()
    count = None

    class Meta:
        model = Contract
        fields = ('date', 'sum')


class DateCountSoloContractStatsSerializer(BaseDateCountStatsSerializer):

    class Meta(BaseDateCountStatsSerializer.Meta):
        model = SoloContract


class DateSumSoloContractStatsSerializer(BaseDateCountStatsSerializer):
    sum = serializers.IntegerField()
    count = None

    class Meta:
        model = SoloContract
        fields = ('date', 'sum')
