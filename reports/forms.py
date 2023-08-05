from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ReportResponse
from .enums import ReportResponseChoices


class ChoiceOrTextWidget(forms.MultiWidget):

    def get_choice_widget(self):
        for widget in self.widgets:
            if isinstance(widget, forms.Select):
                return widget
        return None

    def get_choices(self):
        widget = self.get_choice_widget()
        if widget:
            return widget.choices
        return ()

    def prepare_value(self, value):
        if value is not None and value.startswith('[') and value.endswith(']'):
            value = list(map(int, value[1:-1].replace("'", "").split(',')))
        return value

    def is_choice_value(self, value):
        if isinstance(value, (list, tuple)):
            return True
        return value in [v for k, v in self.get_choices()]

    def decompress(self, value):
        value = self.prepare_value(value)
        # this might need to be tweaked if the name of a choice != value of a choice
        if value:  # indicates we have a updating object versus new one
            if self.is_choice_value(value):
                return value, ""  # make it set the dropdown to choice
            else:
                return "", value  # keep dropdown to blank, set freetext
        return "", ""  # default for new object


class ChoiceOrTextField(forms.MultiValueField):
    widget = ChoiceOrTextWidget

    def __init__(self, choices, max_length=80, *args, **kwargs):
        """"""

        fields = (
            forms.MultipleChoiceField(choices=choices, required=False),
            forms.CharField(max_length=max_length, required=False)
        )

        self.widget = self.get_widget(widgets=[f.widget for f in fields])

        super().__init__(required=False, fields=fields, *args, **kwargs)

    def get_widget_class(self):
        return self.widget

    def get_widget(self, *args, **kwargs):
        Widget = self.get_widget_class()
        return Widget(*args, **kwargs)

    def compress(self, data_list):
        """ return the choicefield value if selected or char field value (if both empty, will throw exception """
        if not data_list:
            raise forms.ValidationError(_('Need to select choice or enter text for this field'))
        return data_list[0] or data_list[1]


class ReportResponseForm(forms.ModelForm):
    response = ChoiceOrTextField(choices=ReportResponseChoices.choices)

    class Meta:
        model = ReportResponse
        exclude = ('user', 'create_at', 'update_at')
