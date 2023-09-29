from django.urls import path
from django.contrib.admin import AdminSite
from django.utils.functional import LazyObject
from django.template.response import TemplateResponse
from rest_framework_simplejwt.tokens import RefreshToken

from .views import SendEmailView


class CustomAdminSite(AdminSite):
    final_catch_all_view = False

    def charts_view(self, request, extra_context=None):
        app_list = self.get_app_list(request)

        refresh = RefreshToken.for_user(request.user)

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
            'token': str(refresh.access_token)
        }
        request.current_app = self.name

        return TemplateResponse(request, "admin/charts.html", context)

    def send_email_view(self, request, extra_context=None):
        defaults = {
            'extra_context': {**self.each_context(request), **(extra_context or {})},
            'template_name': 'admin/send_email.html'
        }
        request.current_app = self.name
        return SendEmailView.as_view(**defaults)(request)

    def get_urls(self):
        urlpatterns = super().get_urls()
        urlpatterns += [
            path("charts/", self.charts_view, name="charts"),
            path("send-email/", self.send_email_view, name="send_email"),
        ]
        return urlpatterns


class DefaultAdminSite(LazyObject):

    def _setup(self):
        self._wrapped = CustomAdminSite()

    def __repr__(self):
        return repr(self._wrapped)


admin_site = DefaultAdminSite()
