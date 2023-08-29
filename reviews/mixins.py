from django.contrib import admin


class AdminContextMixin:
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data() as the template context for admin page.
    """

    extra_context = None

    def get_context_data(self, context):
        context = context or {}
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context

    @admin.options.csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        context = self.get_context_data(extra_context)
        return super().changelist_view(request, context)

    def add_view(self, request, form_url='', extra_context=None):
        context = self.get_context_data(extra_context)
        return super().add_view(request, form_url, context)

    def history_view(self, request, object_id, extra_context=None):
        context = self.get_context_data(extra_context)
        return super().delete_view(request, object_id, context)

    @admin.options.csrf_protect_m
    def delete_view(self, request, object_id, extra_context=None):
        context = self.get_context_data(extra_context)
        return super().delete_view(request, object_id, context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = self.get_context_data(extra_context)
        return super().change_view(request, object_id, form_url, context)
