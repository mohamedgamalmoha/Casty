from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RateListFilter(admin.SimpleListFilter):
    title = _('Rate')
    parameter_name = 'rate'

    def lookups(self, request, model_admin):
        return (
            (0, _('0')),
            (1, _('1')),
            (2, _('2')),
            (3, _('3')),
            (4, _('4')),
            (5, _('5')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val is None:
            return queryset
        return queryset.filter(rate=val)


class RangeFilter(admin.ListFilter):
    title = 'Range'
    parameter_name = 'range'
    template = 'admin/range.html'

    def __init__(self, request, params, model, model_admin, min_range_value=0, max_range_value=10):
        super().__init__(request, params, model, model_admin)

        self.request = request
        # Those values used to determine the limits of the range input
        self.min_range_value = min_range_value
        self.max_range_value = max_range_value

        for expected_parameter in self.expected_parameters():
            if expected_parameter in params:
                value = params.pop(expected_parameter)
                self.used_parameters[expected_parameter] = value

    def choices(self, changelist):
        return ()

    def queryset(self, request, queryset):
        try:
            return queryset.filter(**self.used_parameters)
        except (ValueError, ValidationError) as e:
            # Fields may raise a ValueError or ValidationError when converting
            # the parameters to the correct type.
            raise admin.options.IncorrectLookupParameters(e)

    def expected_parameters(self):
        return [f"{self.parameter_name}__gte", f"{self.parameter_name}__lte"]

    def has_output(self):
        return True
