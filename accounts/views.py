from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from djoser.compat import get_user_email

from .forms import SendEmailForm
from .wrapper import EmailWrapper


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
        for user in users:
            context['user'] = user
            to = [get_user_email(user)]
            EmailWrapper(self.request, context, url_name='default').send(to)
        return super().form_valid(form)
