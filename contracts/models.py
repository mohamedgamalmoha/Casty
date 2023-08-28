from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError, MinValueValidator, MaxValueValidator

from djmoney.money import Money
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

from agencies.models import Agency
from agencies.enums import IndustryChoices
from profiles.models import Language, Skill, Profile
from profiles.enums import GenderChoices, HairColorChoices, EyeColorChoices, RaceChoices
from .enums import StatusChoices


class BaseContract(models.Model):

    # Main Information
    industry = models.PositiveSmallIntegerField(null=True, blank=True, choices=IndustryChoices.choices,
                                                verbose_name=_('Industry'))
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"),
                                   help_text=_('Describe the role of the model'))
    guidelines = models.TextField(null=True, blank=True, verbose_name=_("Guidelines"),
                                  help_text=_('Provide guidelines for the models applying to this contract'))
    restrictions = models.TextField(null=True, blank=True, verbose_name=_("Restriction"),
                                    help_text=_('List any restrictions or things that are not allowed to be done'))
    money_offer = MoneyField(max_digits=20, decimal_places=4,
                             validators=[
                                 MinMoneyValidator(Money(10, settings.DEFAULT_CURRENCY)),
                                 MaxMoneyValidator(Money(1_000_000, settings.DEFAULT_CURRENCY))
                             ],
                             verbose_name=_('Money Offer'))
    start_at = models.DateTimeField(verbose_name=_('Start Date'))

    # Movement Restriction
    require_travel_inboard = models.BooleanField(null=True, blank=True, verbose_name=_('Requires Travel Inboard'),
                                                 help_text=_('Does the location requires travel inboard / locally?'))
    require_travel_outboard = models.BooleanField(null=True, blank=True, verbose_name=_('Requires Travel outboard'),
                                                  help_text=_('Does the location requires travel outboard / globally?'))
    num_of_days = models.PositiveSmallIntegerField(null=True, blank=True,
                                                   validators=[MinValueValidator(1), MaxValueValidator(365)],
                                                   verbose_name=_('Number Of Days'),
                                                   help_text=_('How many days does the location last?'))

    # Current Location
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Country'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))

    class Meta:
        abstract = True


class Contract(BaseContract):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='contracts', verbose_name=_('Agency'))

    num_of_models = models.PositiveSmallIntegerField(null=True, blank=True,
                                                     validators=[MinValueValidator(1), MaxValueValidator(100)],
                                                     verbose_name=_('Number Of Models'),
                                                     help_text=_('How many models does the location need?'))

    # Personal Details
    skills = models.ManyToManyField(Skill, blank=True, verbose_name=_('Skills'))
    languages = models.ManyToManyField(Language, blank=True, verbose_name=_('Languages'))

    gender = models.PositiveSmallIntegerField(choices=GenderChoices.choices, default=GenderChoices.MALE, null=True,
                                              blank=True, verbose_name=_('Gender'))
    race = models.PositiveSmallIntegerField(choices=RaceChoices.choices, default=RaceChoices.OTHER, null=True,
                                            blank=True, verbose_name=_('Race'))

    # Physical Attributes
    hair = models.PositiveSmallIntegerField(null=True, blank=True, choices=HairColorChoices.choices,
                                            verbose_name=_('Hair Color'))
    eye = models.PositiveSmallIntegerField(null=True, blank=True, choices=EyeColorChoices.choices,
                                           verbose_name=_('Eye Color'))
    age_min = models.PositiveSmallIntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(4), MaxValueValidator(100)],
                                               verbose_name=_('Minimum Age'))
    age_max = models.PositiveSmallIntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(4), MaxValueValidator(100)],
                                               verbose_name=_('Maximum Age'))
    height_min = models.PositiveSmallIntegerField(null=True, blank=True,
                                                  validators=[MinValueValidator(50), MaxValueValidator(250)],
                                                  verbose_name=_('Minimum Height'))
    height_max = models.PositiveSmallIntegerField(null=True, blank=True,
                                                  validators=[MinValueValidator(50), MaxValueValidator(250)],
                                                  verbose_name=_('Maximum Height'))
    weight_min = models.PositiveSmallIntegerField(null=True, blank=True,
                                                  validators=[MinValueValidator(30), MaxValueValidator(250)],
                                                  verbose_name=_('Minimum Weight'))
    weight_max = models.PositiveSmallIntegerField(null=True, blank=True,
                                                  validators=[MinValueValidator(30), MaxValueValidator(250)],
                                                  verbose_name=_('Maximum Weight'))

    # Others
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'),
                                    help_text=_('Designates whether contract is viewed for models'))

    # Manipulation Attributes
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        ordering = ('-create_at', '-update_at')

    def save(self, *args, **kwargs):
        if self.start_at and (self.start_at <= timezone.now() + timezone.timedelta(days=1)):
            raise ValidationError(_("Start date must be at least one day ahead of the day of creation."))
        if (self.age_min and self.age_max) and (self.age_min > self.age_max):
            raise ValidationError(_("Minimum age cant be greater than maximum"))
        if (self.height_min and self.height_max) and (self.height_min > self.height_max):
            raise ValidationError(_("Minimum height cant be greater than maximum"))
        if (self.weight_min and self.weight_max) and (self.weight_min > self.weight_max):
            raise ValidationError(_("Minimum weight cant be greater than maximum"))
        if (self.require_travel_inboard is not None and self.require_travel_outboard is not None) and \
                (self.require_travel_inboard and self.require_travel_outboard):
            raise ValidationError(_("Location cant require travelling inboard and outboard at the same time"))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContractRequest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contract_requests', verbose_name=_('Profile'))
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='requests',
                                 verbose_name=_('Contract'))
    model_notes = models.TextField(blank=True, verbose_name=_('Director Notes'))
    status = models.PositiveSmallIntegerField(choices=StatusChoices.choices, default=StatusChoices.PENDING, null=True,
                                              blank=True, verbose_name=_('Status'))
    money_offer = MoneyField(null=True, blank=True, max_digits=20, decimal_places=4,
                             validators=[
                                 MinMoneyValidator(Money(10, settings.DEFAULT_CURRENCY)),
                                 MaxMoneyValidator(Money(1_000_000, settings.DEFAULT_CURRENCY))
                             ],
                             verbose_name=_('Money Offer'))
    director_notes = models.TextField(blank=True, verbose_name=_('Director Notes'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Contract Request')
        verbose_name_plural = _('Contract Requests')
        ordering = ('-create_at', '-update_at')

    @property
    def inboard_score(self):
        return self.contract.require_travel_inboard == self.profile.travel_inboard

    @property
    def outboard_score(self):
        return self.contract.require_travel_outboard == self.profile.travel_outboard

    @property
    def days_score(self):
        return self.contract.num_of_days <= self.profile.days_away

    @property
    def skills_score(self):
        contract_skills = self.contract.skills.all()
        all_skills_count = contract_skills.count()
        intersection_skills_count = contract_skills.intersection(self.profile.skills.all()).count()
        return intersection_skills_count / all_skills_count

    @property
    def languages_score(self):
        contract_languages = self.contract.languages.all()
        all_languages_count = contract_languages.count()
        intersection_languages_count = contract_languages.intersection(self.profile.languages.all()).count()
        return intersection_languages_count / all_languages_count

    @property
    def gender_score(self):
        return self.contract.gender == self.profile.gender

    @property
    def race_score(self):
        return self.contract.race == self.profile.race

    @property
    def hair_score(self):
        return self.contract.hair == self.profile.hair

    @property
    def eye_score(self):
        return self.contract.eye == self.profile.eye

    @property
    def age_score(self):
        return self.contract.age_min < self.profile.age < self.contract.age_max

    @property
    def height_score(self):
        return self.contract.height_min < self.profile.height < self.contract.height_max

    @property
    def weight_score(self):
        return self.contract.height_min < self.profile.height < self.contract.height_max

    @property
    def scores(self):
        return [
            self.inboard_score,
            self.outboard_score,
            self.days_score,
            self.skills_score,
            self.languages_score,
            self.gender_score,
            self.race_score,
            self.hair_score,
            self.eye_score,
            self.age_score,
            self.height_score,
            self.weight_score
        ]

    @property
    def matching_score(self):
        scores = self.scores
        return sum(scores) / len(scores)


class SoloContract(BaseContract):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requests', verbose_name=_('Profile'))
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='solo_contracts', verbose_name=_('Agency'))
    model_notes = models.TextField(blank=True, verbose_name=_('Director Notes'))
    status = models.PositiveSmallIntegerField(choices=StatusChoices.choices, default=StatusChoices.PENDING, null=True,
                                              blank=True, verbose_name=_('Status'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Solo Contract')
        verbose_name_plural = _('Solo Contracts')
        ordering = ('-create_at', '-update_at')


@receiver(post_save, sender=ContractRequest)
def assign_money_offer(sender, instance, created, *args, **kwargs):
    # Assign contract`s money offer as default for contract request
    if created and instance and not instance.money_offer and instance.contract and instance.contract.money_offer:
        instance.money_offer = instance.cotract.money_offer
        instance.save()
