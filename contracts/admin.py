from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Contract, ContractRequest, SoloContract


class ContractRequestInlineAdmin(admin.TabularInline):
    model = ContractRequest
    readonly_fields = ('create_at', 'update_at')
    extra = 0
    min_num = 0
    can_delete = False


class ContractAdmin(admin.ModelAdmin):
    list_display = ['agency', 'industry', 'num_of_models', 'is_active', 'create_at', 'update_at']
    search_fields = ['title', 'description', 'guidelines', 'restrictions']
    list_filter = ['industry', 'require_travel_inboard', 'require_travel_outboard', 'gender', 'race', 'hair', 'eye',
                   'is_active']
    date_hierarchy = 'create_at'
    list_per_page = 20
    readonly_fields = ['create_at', 'update_at']
    inlines = [ContractRequestInlineAdmin]
    fieldsets = (
        (_('Main Info'), {'fields': ('agency', 'industry', 'is_active', 'title', 'description', 'guidelines',
                                     'restrictions')}),
        (_('Details'), {'fields': ('money_offer', 'num_of_models', 'start_at', 'require_travel_inboard',
                                   'require_travel_outboard', 'num_of_days')}),
        (_('Skills'), {'fields': ('skills', 'languages')}),
        (_('Physical Attributes'), {'fields': ('gender', 'race', 'hair', 'eye', ('age_min', 'age_max'), ('height_min',
                                               'height_max'), ('weight_min', 'weight_max'))}),
        (_('Address'), {'fields': ('city', 'country', 'address')}),
        (_('Dates'), {'fields': ('create_at', 'update_at')}),
    )


class SoloContractAdmin(admin.ModelAdmin):
    list_display = ['agency', 'profile', 'industry', 'status', 'create_at', 'update_at']
    search_fields = ['title', 'description', 'guidelines', 'restrictions', 'model_notes']
    list_filter = ['industry', 'require_travel_inboard', 'require_travel_outboard', 'status']
    date_hierarchy = 'create_at'
    list_per_page = 20
    readonly_fields = ['create_at', 'update_at']
    fieldsets = (
        (_('Main Info'), {'fields': ('agency', 'profile', 'status', 'industry', 'title', 'description', 'guidelines',
                                     'restrictions')}),
        (_('Details'), {'fields': ('money_offer', 'start_at', 'require_travel_inboard', 'require_travel_outboard',
                                   'num_of_days')}),
        (_('Model Notes'), {'fields': ('model_notes', )}),
        (_('Address'), {'fields': ('city', 'country', 'address')}),
        (_('Dates'), {'fields': ('create_at', 'update_at')}),
    )


admin.site.register(Contract, ContractAdmin)
admin.site.register(SoloContract, SoloContractAdmin)
