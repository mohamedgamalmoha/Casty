from django_filters import rest_framework as filters

from reviews.models import Rate
from reports.models import Report
from accounts.models import User
from accounts.enums import RoleChoices
from contracts.models import Contract, SoloContract


class UserStatsFilter(filters.FilterSet):
    role = filters.ChoiceFilter(choices=RoleChoices.exclude_admin())
    date_joined = filters.NumberFilter(field_name='date_joined', lookup_expr='day')
    date_joined_day__gt = filters.NumberFilter(field_name='date_joined', lookup_expr='day__gt')
    date_joined_day__lt = filters.NumberFilter(field_name='date_joined', lookup_expr='day__lt')

    class Meta:
        model = User
        fields = ('date_joined', 'role')


class BaeCreateAtStatsFilter(filters.FilterSet):
    create_at = filters.NumberFilter(field_name='create_at', lookup_expr='day')
    create_at_day__gt = filters.NumberFilter(field_name='create_at', lookup_expr='day__gt')
    create_at_day__lt = filters.NumberFilter(field_name='create_at', lookup_expr='day__lt')

    class Meta:
        fields = ('create_at', )


class ReportStatsFilter(BaeCreateAtStatsFilter):

    class Meta:
        model = Report
        fields = ('user', 'is_active', 'type', 'create_at')


class RateStatsFilter(BaeCreateAtStatsFilter):

    class Meta:
        model = Rate
        fields = ('agency', 'profile', 'is_active', 'create_at')


class ContractStatsFilter(BaeCreateAtStatsFilter):

    class Meta:
        model = Contract
        fields = ('industry', 'money_offer', 'money_offer_currency', 'start_at', 'require_travel_inboard',
                  'require_travel_outboard', 'num_of_days', 'agency', 'num_of_models', 'gender', 'race', 'hair', 'eye',
                  'age_min', 'age_max', 'height_min', 'height_max', 'weight_min', 'weight_max', 'skills', 'languages',
                  'is_active', 'create_at')


class SoloContractStatsFilter(BaeCreateAtStatsFilter):

    class Meta:
        model = SoloContract
        fields = ('industry', 'title', 'description', 'guidelines', 'restrictions', 'money_offer_currency',
                  'money_offer', 'start_at', 'require_travel_inboard', 'require_travel_outboard', 'num_of_days',
                  'profile', 'agency', 'model_notes', 'status', 'create_at')
