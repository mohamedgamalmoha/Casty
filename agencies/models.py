from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from accounts.enums import RoleChoices
from accounts.models import CustomUserManager
from .enums import ServiceChoices, IndustryChoices


User = get_user_model()


class DirectorUserManager(CustomUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=RoleChoices.DIRECTOR)


class DirectorUser(User):

    base_role = RoleChoices.MODEL

    student = DirectorUserManager()

    class Meta:
        proxy = True


class AgencyQuerySet(models.QuerySet):

    def with_since_years(self):
        current_date = localdate().today()
        return self.exclude(since__isnull=True).annotate(
            since_years=current_date.year - models.F('since__year')
        )

    def since_years_range(self, start, end):
        return self.with_since_years().filter(since_years__gte=start, since_years__lte=end)


class AgencyManager(models.Manager):

    def get_queryset(self):
        return AgencyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().filter(user__is_active=True)

    def since_years_range(self, start, end):
        return self.get_queryset().since_years_range(start, end)


class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency', verbose_name=_('User'))
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Name'))
    about = models.TextField(null=True, blank=True, verbose_name=_('About'))
    since = models.DateField(null=True, blank=True, verbose_name=_('Since'))
    is_authorized = models.BooleanField(null=True, blank=True, default=False, verbose_name=_('Is Authorized'))

    # Contact Information
    email = models.EmailField(null=True, blank=True, verbose_name=_('Email Address'))
    phone_number_1 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 1'))
    phone_number_2 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 2'))

    # Current Location
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Country'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))
    latitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)],
                                 verbose_name=_('Latitude'))
    longitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                  verbose_name=_('Longitude'))

    # Services Offered
    service = models.PositiveSmallIntegerField(null=True, blank=True, choices=ServiceChoices.choices,
                                               verbose_name=_('Service'))
    industry = models.PositiveSmallIntegerField(null=True, blank=True, choices=IndustryChoices.choices,
                                                verbose_name=_('Industry'))

    # Manipulation Attributes
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = AgencyManager()

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')
        ordering = ['-create_at', '-update_at']


class PreviousWork(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='works', verbose_name=_('Agency'))
    project_name = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Project Name'))
    client_name = models.CharField(null=True, blank=True, max_length=200, verbose_name=_('Client Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    success_story = models.TextField(null=True, blank=True, verbose_name=_('Success Story'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'),
                                help_text=_('If the project is ongoing, the end_date can be null'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'),
                                    help_text=_('Designates whether experience is viewed at the profile'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Previous Work')
        verbose_name_plural = _('Previous Works')
        ordering = ('-create_at', '-update_at')


@receiver(post_save, sender=User)
def create_director_agency(sender, instance, created, *args, **kwargs):
    if created and instance and instance.role == RoleChoices.DIRECTOR:
        instance.agency = Agency.objects.create(user=instance)
