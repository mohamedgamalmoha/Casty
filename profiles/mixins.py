

class AdminQueryset:
    queryset = None

    def get_queryset(self, request):
        if self.queryset is None:
            qs = self.model._default_manager.get_queryset()
        else:
            qs = self.queryset
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
