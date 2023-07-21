from django.db import models
from django.utils.translation import gettext_lazy as _


class IndustryChoices(models.IntegerChoices):
    FILM = 0, _('Film')
    CINEMA = 1, _('Cinema')
    FASHION = 2, _('Fashion')
    TELEVISION = 3, _('Television')
    COMMERCIALS = 4, _('Commercials')
    THEATER = 5, _('Theater')
    MIXED = 6, _('Mixed')
    OTHER = 7, _('Other')


class ServiceChoices(models.IntegerChoices):
    MODELS = 0, _('Models')
    ACTORS = 1, _('Actors')
    EXTRAS = 2, _('Extras')
    MIXED = 3, _('Mixed')
