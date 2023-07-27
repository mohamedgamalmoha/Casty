from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from agencies.models import Agency
from accounts.enums import RoleChoices
from accounts.models import CustomUserManager
from .utils import get_hostname_from_url
from .enums import GenderChoices, RaceChoices, HairColorChoices, EyeColorChoices

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    is_active = models.BooleanField(null=True, blank=True, default=True, verbose_name=_('Is Active'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['-create_at', '-update_at']

    def __str__(self):
        return str(self.name)


class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    code = models.CharField(max_length=5, null=True, blank=True, verbose_name=_('Code'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['-create_at', '-update_at']

    def __str__(self):
        return str(self.name)


class ModelUserManager(CustomUserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=RoleChoices.MODEL)


class ModelUser(User):
    base_role = RoleChoices.MODEL

    student = ModelUserManager()

    class Meta:
        proxy = True


class ProfilerQuerySet(models.QuerySet):

    def with_age(self):
        current_date = localdate().today()
        return self.exclude(date_of_birth__isnull=True).annotate(
            age=models.ExpressionWrapper(
                current_date.year - models.F('date_of_birth__year') -
                models.Case(
                    models.When(
                        models.Q(date_of_birth__month__gt=current_date.month) |
                        models.Q(date_of_birth__month=current_date.month, date_of_birth__day__gt=current_date.day),
                        then=models.Value(1)
                    ),
                    default=models.Value(0),
                    output_field=models.IntegerField()
                ),
                output_field=models.IntegerField()
            )
        )

    def age_range(self, start, end):
        return self.with_age().filter(age__gte=start, age__lte=end)


class ProfileManager(models.Manager):

    def get_queryset(self):
        return ProfilerQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().filter(user__is_active=True)

    def age_range(self, start, end):
        return self.get_queryset().age_range(start, end)


class Profile(models.Model):
    user = models.OneToOneField(ModelUser, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    is_public = models.BooleanField(null=True, blank=True, default=True, verbose_name=_('Is Public'))

    # Following
    following_models = models.ManyToManyField('self', blank=True, related_name='follower_models',
                                              verbose_name=_('Following Models'))
    following_agencies = models.ManyToManyField(Agency, blank=True, related_name='follower_agencies',
                                                verbose_name=_('Following Agencies'))

    # Personal Details
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))
    skills = models.ManyToManyField(Skill, blank=True, verbose_name=_('Skills'))
    languages = models.ManyToManyField(Language, blank=True, verbose_name=_('Languages'))
    gender = models.PositiveSmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MALE, null=True,
                                              blank=True, verbose_name=_('Gender'))
    race = models.PositiveSmallIntegerField(choices=RaceChoices.choices, default=RaceChoices.OTHER, null=True,
                                            blank=True, verbose_name=_('Race'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))

    # Contact Information
    phone_number_1 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 1'))
    phone_number_2 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 2'))

    # Current Location
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Country'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))

    # Movement Restriction
    travel_inboard = models.BooleanField(null=True, blank=True,
                                         verbose_name=_('Travel Inboard'),
                                         help_text=_('Willingness to travel inboard / locally'))
    travel_outboard = models.BooleanField(null=True, blank=True,
                                          verbose_name=_('Travel outboard '),
                                          help_text=_('Willingness to travel outboard / globally'))
    days_away = models.PositiveSmallIntegerField(null=True, blank=True,
                                                 validators=[MinValueValidator(1), MaxValueValidator(365)],
                                                 verbose_name=_('Days Away'),
                                                 help_text=_('How many days can you stay away from home?'))
    # Physical Attributes
    height = models.PositiveSmallIntegerField(null=True, blank=True,
                                              validators=[MinValueValidator(50), MaxValueValidator(250)],
                                              verbose_name=_('Height'))
    weight = models.PositiveSmallIntegerField(null=True, blank=True,
                                              validators=[MinValueValidator(30), MaxValueValidator(250)],
                                              verbose_name=_('Weight'))
    hair = models.PositiveSmallIntegerField(null=True, blank=True, choices=HairColorChoices.choices,
                                            verbose_name=_('Hair Color'))
    eye = models.PositiveSmallIntegerField(null=True, blank=True, choices=EyeColorChoices.choices,
                                           verbose_name=_('Eye Color'))

    # Image
    image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name=_('Image'))
    cover = models.ImageField(null=True, blank=True, upload_to='covers/', verbose_name=_('Cover Image'))

    # Manipulation Attributes
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = ProfileManager()

    def __str__(self) -> str:
        return getattr(self.user, 'get_full_name', lambda: '')()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-create_at', '-update_at']


class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links', verbose_name=_('Profile'))
    url = models.URLField(blank=False, null=False, verbose_name=_('Link'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'),
                                    help_text=_('Designates whether this link is viewed at the profile'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.domain

    @property
    def domain(self):
        return get_hostname_from_url(self.url)


class PreviousExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences',
                                verbose_name=_('Profile'))
    company_name = models.CharField(max_length=255, verbose_name=_('Company Name'))
    project_name = models.CharField(max_length=100, verbose_name=_('Project Name'))
    role = models.CharField(max_length=100, verbose_name=_('Role'))
    description = models.TextField(verbose_name=_('Description'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'),
                                help_text=_('If the project is ongoing, the end_date can be null'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'),
                                    help_text=_('Designates whether experience is viewed at the profile'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')
        ordering = ('-create_at', '-update_at')


class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images', verbose_name=_('Profile'))
    image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name=_('Image'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'),
                                    help_text=_('Designates whether images is viewed at the profile'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    MAXIMUM_NUMBER = 5

    class Meta:
        verbose_name = _('Profile Image')
        verbose_name_plural = _('Profile Images')
        ordering = ('-create_at', '-update_at')


@receiver(post_save, sender=User)
def create_model_profile(sender, instance, created, *args, **kwargs):
    if created and instance and instance.role == RoleChoices.MODEL:
        instance.profile = Profile.objects.create(user=instance)


@receiver(pre_delete, sender=Profile)
def delete_model_photos(sender, instance, *args, **kwargs):
    image = instance.image
    if image:
        image.delete(save=False)

    cover = instance.cover
    if cover:
        cover.delete(save=False)


@receiver(pre_delete, sender=ProfileImage)
def delete_profile_photos(sender, instance, *args, **kwargs):
    image = instance.image
    if image:
        image.delete(save=False)
