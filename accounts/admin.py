from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _, ngettext

from social_django.models import UserSocialAuth, Nonce, Association
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import User


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


admin.site.unregister(Nonce)
admin.site.unregister(Association)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
admin.site.register(User, CustomUserAdmin)
