from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from djoser.compat import get_user_email

from .email import DefaultEmail
from .forms import SendEmailForm


class SendEmailView(SuccessMessageMixin, FormView):
    form_class = SendEmailForm
    success_message = _('Emails are sent successfully')

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        users = form.get_users()
        context = {
            'subject': form.cleaned_data['subject'],
            'body': form.cleaned_data['body']
        }
        # TODO: Integrate with async-proj branch to use EmailWrapper.
        to = list(map(get_user_email, users))
        DefaultEmail(self.request, context).send(to)
        return super().form_valid(form)
