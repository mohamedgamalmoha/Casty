from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _, ngettext

from djoser.compat import get_user_email
from djmoney.contrib.exchange.models import Rate
from djmoney.contrib.exchange.admin import RateAdmin

from .models import User
from .sites import admin_site
from .wrapper import EmailWrapper


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    actions = ['activate_users', 'deactivate_users']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'groups')

    def get_inlines(self, request, obj):
        if not obj or (obj and (obj.is_staff or obj.is_superuser)):
            return []
        return self.inlines

    def deactivate_users(self, request, queryset):
        updated = queryset.filter(is_active=True).update(is_active=False)
        for user in updated:
            context = {'user': user}
            to = [get_user_email(user)]
            EmailWrapper(request, context, url_name='user-activation').send(to)
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user was successfully deactivated.",
                    "%d users were successfully deactivated.",
                    updated,
                ) % updated
            ),
            messages.SUCCESS,
        )

    deactivate_users.short_description = _('Deactivate selected Users')

    def activate_users(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        for user in updated:
            context = {'user': user}
            to = [get_user_email(user)]
            EmailWrapper(request, context, url_name='user-confirmation').send(to)
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user was successfully activated.",
                    "%d users were successfully activated.",
                    updated,
                ) % updated
            ),
            messages.SUCCESS,
        )

    activate_users.short_description = _('Activate selected Users')


admin_site.register(Rate, RateAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(User, CustomUserAdmin)
