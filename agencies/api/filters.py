from django.db import models

from django_filters import rest_framework as filters

from agencies.models import Agency, PreviousWork


class AgencyFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search names, and about")

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) | models.Q(about__icontains=value)
        )

    class Meta:
        model = Agency
        fields = ('is_authorized', 'service', 'industry',  'search')


class PreviousWorkFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search',
                                label="Search project name, client name, description, and success story")

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(project_name__icontains=value) | models.Q(client_name__icontains=value) |
            models.Q(description__icontains=value) | models.Q(success_story__icontains=value)
        )

    class Meta:
        model = PreviousWork
        fields = ('is_active', 'search', 'start_date', 'end_date')
