from django.db import models
from django_filters import rest_framework as filters

from contracts.utils import get_model_field_names
from contracts.models import Contract, ContractRequest, SoloContract


class CustomSearchFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search in title & description & guidelines & restrictions")
    location = filters.CharFilter(method='custom_location', label="Search in city & country & address")

    def custom_search(self, queryset, name, value):
        """Search in title & description & guidelines & restrictions"""
        return queryset.filter(
            models.Q(title__icontains=value) | models.Q(description__icontains=value) |
            models.Q(guidelines__icontains=value) | models.Q(restrictions__icontains=value)
        )

    def custom_location(self, queryset, name, value):
        """Search in city & country & address"""
        return queryset.filter(
            models.Q(city__icontains=value) | models.Q(country__icontains=value) | models.Q(address__icontains=value)
        )


class ContractFilter(CustomSearchFilter):

    class Meta:
        model = Contract
        fields = (
            *get_model_field_names(Contract, ['id', 'is_active', 'create_at', 'update_at']),
            'search', 'location'
        )


class ContractRequestFilter(CustomSearchFilter):

    class Meta:
        model = ContractRequest
        exclude = ('create_at', 'update_at')


class SoloContractFilter(CustomSearchFilter):

    class Meta:
        model = SoloContract
        fields = (
            *get_model_field_names(SoloContract, ['id', 'create_at', 'update_at']),
            'search', 'location'
        )
