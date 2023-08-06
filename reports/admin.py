from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .forms import ReportResponseForm
from .utils import get_change_admin_url
from .models import Report, ReportResponse


class ReportResponseInlineAdmin(admin.TabularInline):
    model = ReportResponse
    form = ReportResponseForm
    readonly_fields = ('user', 'create_at', 'update_at')
    can_delete = False
    min_num = 0
    extra = 0


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'create_at', 'update_at')
    list_filter = ('type', 'is_active')
    readonly_fields = ('object_link', 'create_at', 'update_at')
    exclude = ('content_type', 'object_id', 'content_object')
    inlines = [ReportResponseInlineAdmin]
    fieldsets = (
        (_('General'), {'fields': ('user', 'type', 'title', 'content', 'attachment', 'is_active', 'object_link',
                                   'create_at', 'update_at')}),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def object_link(self, obj):
        name = str(obj.content_object)
        link = get_change_admin_url(obj.content_object)
        return mark_safe(f"<a href='{link}'> {name} </a>")

    object_link.short_description = _('Reported Object Link')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in filter(lambda obj: isinstance(obj, ReportResponse) and not obj.user, instances):
            instance.user = request.user
        formset.save()


admin.site.register(Report, ReportAdmin)
