from django import forms
from django.utils.translation import gettext_lazy as _

from jazzmin.widgets import JazzminSelect, JazzminSelectMultiple

from .models import User
from .enums import RoleChoices


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
