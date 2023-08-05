from django.db import models

from django_filters import rest_framework as filters

from reports.models import Report


class ReportFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search title & content")

    def custom_search(self, queryset, name, value):
        """Search first & last & nick name, and email"""
        return queryset.filter(
            models.Q(title__icontains=value) | models.Q(content__icontains=value)
        )

    class Meta:
        model = Report
        fields = ('user', 'type', 'search')
