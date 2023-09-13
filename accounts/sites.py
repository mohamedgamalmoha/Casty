from django.urls import path
from django.contrib.admin import AdminSite
from django.utils.functional import LazyObject
from django.template.response import TemplateResponse
from rest_framework_simplejwt.tokens import RefreshToken


class CustomAdminSite(AdminSite):
    final_catch_all_view = False

    def charts(self, request, extra_context=None):
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

    def get_urls(self):
        urlpatterns = super().get_urls()
        urlpatterns += [
            path("charts/", self.charts, name="charts"),
        ]
        return urlpatterns


class DefaultAdminSite(LazyObject):

    def _setup(self):
        self._wrapped = CustomAdminSite()

    def __repr__(self):
        return repr(self._wrapped)


admin_site = DefaultAdminSite()
