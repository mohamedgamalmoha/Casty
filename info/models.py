from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class MainInfo(models.Model):
    facebook = models.URLField(verbose_name=_('Facebook Link'))
    instagram = models.URLField(verbose_name=_('Instagram Link'))
    twitter = models.URLField(verbose_name=_('Twitter Link'))
    telegram = models.URLField(verbose_name=_('Telegram Link'))
    email = models.EmailField(verbose_name=_('Web Email'))
    whatsapp = PhoneNumberField(null=True, blank=True, verbose_name=_("Whatsapp Number"))
    why_us = models.TextField(null=True, verbose_name=_("Why do you choose us?"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Website Main Info')
        verbose_name_plural = _('Website Main Info')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.email

    def whatsapp_link(self):
        return f"https://wa.me/+2{self.whatsapp}"


class FAQs(models.Model):
    quote = models.CharField(max_length=1000, verbose_name=_("Quote"))
    answer = models.TextField(verbose_name=_("Answer"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Frequently Asked Question')
        verbose_name_plural = _('Frequently Asked Questions')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.quote


class AboutUs(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('About us')
        verbose_name_plural = _('About us')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.title


class TermsOfService(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Terms Of Service')
        verbose_name_plural = _('Terms Of Service')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.title


class CookiePolicy(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Cookie Policy')
        verbose_name_plural = _('Cookie Policy')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.title


class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policy')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    first_name = models.CharField(max_length=120, null=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=120, null=True, verbose_name=_("Last name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"))
    subject = models.CharField(max_length=250, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')
        ordering = ('-create_at', '-update_at')


class HeaderImageManager(models.Manager):

    def active(self):
        return self.filter(is_active=True)


class HeaderImage(models.Model):
    alt = models.CharField(max_length=250, verbose_name=_("Alternative (Alt)"),
                           help_text=_("Text is meant to convey the “why” of the image as it relates to the content of "
                                       "a document or webpage"))
    image = models.ImageField(upload_to='home/header', verbose_name=_("Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"),
                                    help_text=_("Setting it to false, makes the image disappear from homepage"))
    url = models.URLField(null=True, blank=True, verbose_name=_('Link'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = HeaderImageManager()

    def __str__(self):
        return self.alt

    class Meta:
        verbose_name = _('Home Page Image')
        verbose_name_plural = _('Home Page Images')
        ordering = ('-create_at', '-update_at')
