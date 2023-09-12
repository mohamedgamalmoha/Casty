from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from accounts.sites import admin_site
from reports.utils import get_change_admin_url
from .models import Rate
from .filters import RateListFilter


class RateAdmin(admin.ModelAdmin):
    list_display = ('title', 'rate', 'is_active', 'create_at', 'update_at')
    list_filter = (RateListFilter, 'is_active',
                   ('agency', admin.RelatedOnlyFieldListFilter),
                   ('profile', admin.RelatedOnlyFieldListFilter))
    search_fields = ('title', 'comment')
    readonly_fields = ('object_link', 'create_at', 'update_at')
    exclude = ('content_type', 'object_id', 'content_object')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def object_link(self, obj):
        name = str(obj.content_object)
        link = get_change_admin_url(obj.content_object)
        return mark_safe(f"<a href='{link}'> {name} </a>")

    object_link.short_description = _('Rated Object Link')


admin_site.register(Rate, RateAdmin)
