from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator

from agencies.models import Agency
from profiles.models import Profile


class Rate(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='rates',
                               verbose_name=_('Agency'))
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rates', verbose_name=_('Profile'))

    # Fields specific to the rate model
    rate = models.PositiveSmallIntegerField(null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(5)],
                                            verbose_name=_('Rate'))
    title = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Title'))
    comment = models.TextField(null=True, blank=True, verbose_name=_('Comment'))

    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'))

    # Fields for the generic foreign key relation
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')

    # Manipulation Attributes
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')
        ordering = ('-create_at', '-update_at')
        unique_together = ('content_type', 'object_id')  # ensure that every model instance has only one review
        indexes = (
            models.Index(fields=["content_type", "object_id"]),
        )
