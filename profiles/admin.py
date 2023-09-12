from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from accounts.sites import admin_site
from .mixins import AdminQueryset
from .models import Skill, Language, Profile, SocialLink, PreviousExperience, ProfileImage
from .utils import create_html_image


class AgeProfileListFilter(admin.SimpleListFilter):
    title = _('Age')
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        return (
            ('0, 18', _('Under Aage')),
            ('18,30', _('In the twenties')),
            ('30,40', _('In the thirties')),
            ('40,50', _('In the forties')),
            ('50,60', _('In the fifties')),
            ('60,70', _('In the sixties')),
            ('70,80', _('In the seventies')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val is None:
            return queryset
        start_age, end_age = self.value().split(',')
        return queryset.age_range(start_age, end_age)


class SocialLinkInlineAdmin(admin.TabularInline):
    model = SocialLink
    readonly_fields = ('url', 'create_at', 'update_at')
    extra = 0
    min_num = 0
    can_delete = False


class PreviousExperienceInlineAdmin(admin.TabularInline):
    model = PreviousExperience
    readonly_fields = (
        'company_name', 'project_name', 'role', 'description', 'start_date', 'end_date', 'create_at', 'update_at'
    )
    extra = 0
    can_delete = False


class ProfileImageInlineAdmin(admin.TabularInline):
    model = ProfileImage
    readonly_fields = ('image', 'show_image', 'create_at', 'update_at')
    extra = 0
    min_num = 0
    can_delete = False

    def show_image(self, obj):
        return create_html_image(obj.image)

    show_image.short_description = '-'


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'create_at', 'update_at')
    list_filter = ('is_active',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'create_at', 'update_at')


class ProfileAdmin(AdminQueryset, admin.ModelAdmin):
    list_display = ['user', 'create_at', 'update_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'user__email', 'bio']
    date_hierarchy = 'create_at'
    list_filter = ['is_public', 'model_class', 'gender', AgeProfileListFilter, 'race', 'travel_inboard',
                   'travel_outboard', 'hair', 'eye']
    readonly_fields = ['user', 'create_at', 'update_at', 'show_image', 'show_cover']
    fieldsets = (
        (_('User Main Info'), {'fields': (
            'user', 'bio', 'is_public', 'model_class', 'skills', 'languages', 'gender', 'race', 'date_of_birth'
        )}),
        (_('Contact Information'), {'fields': (
            ('phone_number_1', 'phone_number_2'),
        )}),
        (_('Address'), {'fields': (
            'city', 'country', 'address'
        )}),
        (_('Movement Restriction'), {'fields': (
            'travel_inboard', 'travel_outboard', 'days_away'
        )}),
        (_('Physical Attributes'), {'fields': (
            'height', 'weight', 'hair', 'eye'
        )}),
        (_('Images'), {'fields': (
            ('image', 'show_image'),
            ('cover', 'show_cover'),
        )}),
        (_('Following'), {'fields': (
            'following_models', 'following_agencies'
        )}),
        (_('Dates'), {'fields': (
           'create_at', 'update_at'
        )}),
    )

    def show_image(self, obj):
        return create_html_image(obj.image)

    show_image.short_description = '-'

    def show_cover(self, obj):
        return create_html_image(obj.cover)

    show_cover.short_description = '-'

    list_per_page = 20
    queryset = Profile.objects.all()
    inlines = [SocialLinkInlineAdmin, PreviousExperienceInlineAdmin, ProfileImageInlineAdmin]


admin_site.register(Skill, SkillAdmin)
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Language, LanguageAdmin)
