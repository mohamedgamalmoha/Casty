from django.db import models

from django_filters import rest_framework as filters

from profiles.models import Profile, PreviousExperience


class ProfileFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search first & last names, email, username, and bio")

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(user__first_name__icontains=value) | models.Q(user__last_name__icontains=value) |
            models.Q(user__email__icontains=value) | models.Q(user__username__icontains=value) |
            models.Q(bio__icontains=value)
        )

    class Meta:
        model = Profile
        exclude = ('user', 'image', 'cover', 'create_at', 'update_at')
        fields = ('is_public', 'skills', 'languages', 'gender', 'race', 'travel_inboard', 'travel_outboard',
                  'days_away', 'height', 'weight', 'hair', 'eye', 'search')


class PreviousExperienceFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search',
                                label="Search company name, project name, role, and description")

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(company_name__icontains=value) | models.Q(project_name__icontains=value) |
            models.Q(role__icontains=value) | models.Q(description_icontains=value)
        )

    class Meta:
        model = PreviousExperience
        fields = ('search', 'start_date', 'end_date')
