from django.db import models

from django_filters import rest_framework as filters

from accounts.models import User
from accounts.enums import RoleChoices


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search first & last name, username and email")
    role = filters.ChoiceFilter(choices=RoleChoices.exclude_admin())

    def custom_search(self, queryset, name, value):
        """Search first & last & nick name, and email"""
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value) |
            models.Q(email__icontains=value) | models.Q(username__icontains=value)
        )

    class Meta:
        model = User
        fields = ('search', 'role')
