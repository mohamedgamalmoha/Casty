from django.contrib import admin

from .models import Agency, PreviousWork


class PreviousWorkInline(admin.TabularInline):
    model = PreviousWork
    readonly_fields = ('project_name', 'client_name', 'description', 'success_story', 'start_date', 'end_date',
                       'create_at', 'update_at')
    min_num = 0
    extra = 0
    can_delete = False


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_authorized', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at')
    list_filter = ('is_authorized', 'service', 'industry')
    inlines = [PreviousWorkInline]
    fieldsets = (
        ('Agency Main Info', {'fields': (
            'user', 'name', 'about', 'since', 'is_authorized'
        )}),
        ('Contact Information', {'fields': (
            'email', 'phone_number_1', 'phone_number_2'
        )}),
        ('Current Location', {'fields': (
            'city', 'country', 'address', 'latitude', 'longitude'
        )}),
        ('Services Offered', {'fields': (
            'service', 'industry'
        )}),
        ('Following', {'fields': (
            'following_models', 'following_agencies'
        )}),
        ('Dates', {'fields': (
            'create_at', 'update_at'
        )}),
    )
    list_per_page = 20


admin.site.register(Agency, AgencyAdmin)
