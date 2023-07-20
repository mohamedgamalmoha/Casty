from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.IntegerChoices):
    MALE = 1, _("Male")
    FEMALE = 2, _("Female")
    OTHER = 3, _("Other")


class RaceChoices(models.IntegerChoices):
    CAUCASIAN = 0, _('Caucasian / White')
    AFRICAN = 1, _('African / Black')
    ASIAN = 2, _('Asian')
    HISPANIC = 3, _('Hispanic / Latinx')
    NATIVE = 4, _('Native')
    AMERICAN = 5, _('American / Indigenous')
    MIDDLE = 6, _('Middle Eastern')
    EASTERN = 7, _('Eastern')
    PACIFIC = 8, _('Pacific')
    ISLANDER = 9, _('Islander')
    MIXED = 10, _('Mixed / Multiracial')
    OTHER = 11, _('Other')


class HairColorChoices(models.IntegerChoices):
    BLACK = 0, _('Black')
    BROWN = 1, _('Brown (Light, Medium, Dark)')
    BLONDE = 2, _('Blonde (Light, Medium, Dark)')
    RED = 3, _('Red')
    AUBURN = 4, _('Auburn')
    BRUNETTE = 5, _('Brunette')
    CHESTNUT = 6, _('Chestnut')
    SANDY = 7, _('Sandy')
    GRAY = 8, _('Gray / Silver')
    WHITE = 9, _('White')
    BALD = 10, _('Bald')
    OTHER = 11, _('Other')


class EyeColorChoices(models.IntegerChoices):
    BLACK = 0, _('Black')
    BROWN = 1, _('Brown')
    BLUE = 2, _('Blue')
    GREEN = 3, _('Green')
    HAZEL = 4, _('Hazel')
    GRAY = 5, _('Gray')
    AMBER = 6, _('Amber')
    VIOLET = 7, _('Violet')
    OTHER = 8, _('Other')
