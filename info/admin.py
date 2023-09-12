from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from accounts.sites import admin_site
from profiles.utils import create_html_image
from .utils import get_model_fields_names, create_html_icon_link
from .models import (MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, ContactUs, HeaderImage,
                     TeamMember)


class MainInfoAdmin(TranslationAdmin):
    list_display = (
        'email', 'facebook_html_link', 'instagram_html_link', 'twitter_html_link', 'telegram_html_link',
        'whatsapp_html_link', 'create_at', 'update_at'
    )
    fieldsets = (
        (_('Main Info'), {'fields': ('email', 'why_us')}),
        (_('Links'), {'fields': (
            ('facebook', 'facebook_html_link'),
            ('instagram', 'instagram_html_link'),
            ('twitter', 'twitter_html_link'),
            ('telegram', 'telegram_html_link'),
            ('whatsapp', 'whatsapp_html_link'),
        )}),
        (_('Important Dates'), {'fields': ('create_at', 'update_at')}),
    )
    readonly_fields = (
        'facebook_html_link', 'instagram_html_link', 'twitter_html_link', 'telegram_html_link', 'whatsapp_html_link',
        'create_at', 'update_at'
    )

    def has_delete_permission(self, request, obj=None):
        # deny user from deleting the instance
        return False

    def has_add_permission(self, request):
        # Limit main info to only one instance
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def facebook_html_link(self, obj=None):
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'facebook', None), 'facebook')
    facebook_html_link.short_description = _('Facebook Link')

    def instagram_html_link(self, obj=None):
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'instagram', None), 'instagram')
    instagram_html_link.short_description = _('Instagram Link')

    def twitter_html_link(self, obj=None):
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'twitter', None), 'twitter')
    twitter_html_link.short_description = _('Twitter Link')

    def telegram_html_link(self, obj=None):
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'telegram', None), 'telegram')
    telegram_html_link.short_description = _('Telegram Link')

    def whatsapp_html_link(self, obj=None):
        if obj is None:
            return ''
        return create_html_icon_link(getattr(obj, 'whatsapp_link', None), 'whatsapp')
    whatsapp_html_link.short_description = _('Whatsapp Link')


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'subject', 'create_at', 'update_at')
    search_fields = ('email', 'subject', 'first_name', 'last_name', 'message')

    def has_delete_permission(self, request, obj=None):
        # deny user from deleting the instance
        return False

    def has_add_permission(self, request):
        # deny user from adding new instance
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # ensure that all fields are readonly
            return get_model_fields_names(obj, exclude=['id'])
        return super().get_readonly_fields(request, obj)


class TitledDescriptiveTranslationAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'create_at', 'update_at')
    search_fields = ('title', 'description')
    list_per_page = 20
    date_hierarchy = 'create_at'


class FAQsAdmin(TranslationAdmin):
    list_display = ('quote', 'answer', 'create_at', 'update_at')
    search_fields = ('quote', 'answer')


class HeaderImageAdmin(TranslationAdmin):
    list_display = ('alt', 'is_active', 'create_at', 'update_at')
    list_filter = ('is_active', )
    readonly_fields = ('create_at', 'update_at')


class TeamMemberAdmin(TranslationAdmin):
    list_display = ('name', 'position', 'is_active', 'create_at', 'update_at')
    readonly_fields = ('create_at', 'update_at', 'show_image')
    list_filter = ('is_active', )
    search_fields = ('position', 'about')
    fieldsets = (
        (_('Main Info'), {'fields': ('name', 'position', 'about', 'join_date', 'is_active')}),
        (_('Image'), {'fields': ('image', 'show_image')}),
        (_('Dates'), {'fields': ('create_at', 'update_at')}),
    )

    def show_image(self, obj):
        if obj.image:
            return create_html_image(obj.image)
        return ''

    show_image.short_description = ''


admin_site.register(MainInfo, MainInfoAdmin)
admin_site.register(FAQs, FAQsAdmin)
admin_site.register(AboutUs, TitledDescriptiveTranslationAdmin)
admin_site.register(CookiePolicy, TitledDescriptiveTranslationAdmin)
admin_site.register(PrivacyPolicy, TitledDescriptiveTranslationAdmin)
admin_site.register(TermsOfService, TitledDescriptiveTranslationAdmin)
admin_site.register(ContactUs, ContactUsAdmin)
admin_site.register(HeaderImage, HeaderImageAdmin)
admin_site.register(TeamMember, TeamMemberAdmin)
