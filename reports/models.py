from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import ValidationError, FileExtensionValidator

from .enums import ReportTypeChoices
from .validators import FileSizeValidator, FileContentTypeValidator


User = get_user_model()

IMAGES_EXTENSIONS = (
    'jpg',
    'jpeg',
    'png',
    'gif'
)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports', verbose_name=_('User'))

    # Fields specific to the report model
    type = models.PositiveSmallIntegerField(null=True, blank=True, choices=ReportTypeChoices.choices,
                                            default=ReportTypeChoices.OTHER, verbose_name=_('Type'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'))
    attachment = models.FileField(null=True, blank=True, upload_to="attachments/",
                                  validators=[
                                      FileContentTypeValidator(
                                          [
                                              'application/pdf',
                                              *tuple(map(lambda img: f'image/{img}', IMAGES_EXTENSIONS))
                                          ]
                                      ),
                                      FileExtensionValidator(['pdf', *IMAGES_EXTENSIONS]),
                                      FileSizeValidator(size_limit=5),
                                  ],
                                  verbose_name=_('Attachment'))

    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'))

    # Fields for the generic foreign key relation
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')

    # Manipulation Attributes
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ('-create_at', '-update_at')
        indexes = (
            models.Index(fields=["content_type", "object_id"]),
        )


class ReportResponse(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=False, related_name='responses',
                               verbose_name=_('Report'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('User'))
    response = models.TextField(verbose_name=_('Response'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    def save(self, *args, **kwargs):
        if not self.report:
            raise ValidationError(_("Cant create response while being report not active"))
        return super(ReportResponse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Report Response')
        verbose_name_plural = _('Report Responses')
        ordering = ('-create_at', '-update_at')


@receiver(pre_delete, sender=Report)
def delete_attachment(sender, instance, *args, **kwargs):
    file = instance.attachment
    if file:
        file.delete(save=False)
