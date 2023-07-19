from rest_framework import status
from rest_framework.decorators import action

from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema, OpenApiResponse

from accounts.models import User
from accounts.utils import is_non_admin_user
from .filters import UserFilter
from .mixins import DestroyMethodNotAllowedMixin


class UserViewSet(DestroyMethodNotAllowedMixin, DjoserUserViewSet):
    queryset = User.objects.exclude_admin()
    filterset_class = UserFilter

    def get_queryset(self):
        user = self.request.user
        queryset = super(UserViewSet, self).get_queryset()
        if self.action == 'list' and is_non_admin_user(user):
            queryset = queryset.exclude(id=user.id)
        return queryset

    @extend_schema(responses={status.HTTP_405_METHOD_NOT_ALLOWED:
                              OpenApiResponse(description='Delete user is not allowed')})
    def destroy(self, request, *args, **kwargs):
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    @action(["get", "put", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
