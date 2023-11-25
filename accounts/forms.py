from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from jazzmin.widgets import JazzminSelect, JazzminSelectMultiple

from .models import User
from .enums import RoleChoices
from .api.views import UserViewSet


class SendEmailForm(forms.Form):
    users_excluded = forms.ModelMultipleChoiceField(label=_('Users Excluded'), queryset=User.objects.exclude_admin(),
                                                    widget=JazzminSelectMultiple(attrs={'class': 'form-control'}),
                                                    required=False)
    user_type = forms.ChoiceField(label=_('Type of User'),
                                  choices=[(None, '---------'), * RoleChoices.excluded([RoleChoices.ADMIN.value,
                                                                                        RoleChoices.OTHER.value])],
                                  widget=JazzminSelect(attrs={'class': 'form-control'}), required=False)
    subject = forms.CharField(label=_('Subject'), max_length=500,
                              widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    body = forms.CharField(label=_('Body'), widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)

    def get_users(self):
        ids = map(lambda user: user.id, self.cleaned_data['users_excluded'])
        queryset = self.fields['users_excluded'].queryset.exclude(id__in=ids)
        user_type = self.cleaned_data['user_type']
        if user_type:
            queryset = queryset.filter(role=user_type)
        return queryset


class BaseUidAndTokenForm(forms.Form):
    field_name: str
    action_name: str
    uid = forms.CharField(widget=forms.HiddenInput)
    token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def get_viewset(self):
        return UserViewSet.as_view({'post': self.action_name})

    def clean(self):
        cleaned_data = super().clean()
        ViewSet = self.get_viewset()
        response = ViewSet(self.request)
        if response.data:
            for err in response.data.get(self.field_name):
                self.add_error(self.field_name, err)
        return cleaned_data


class ActivationForm(BaseUidAndTokenForm):
    action_name = 'activation'


class ResetUsernameForm(BaseUidAndTokenForm):
    field_name = 'new_email'
    action_name = 'reset_username_confirm'
    new_email = forms.EmailField(
        label=_("New Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class ResetPasswordForm(BaseUidAndTokenForm):
    field_name = 'new_password'
    action_name = 'reset_password_confirm'
    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=True
    )
