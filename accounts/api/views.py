from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from djoser.conf import settings
from djoser.utils import logout_user
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.compat import get_user_email, get_user_email_field_name

from accounts import signals
from accounts.models import User
from accounts.utils import is_non_admin_user
from .filters import UserFilter
from .mixins import DestroyMethodNotAllowedMixin, ProhibitedActionsMixin


class UserViewSet(ProhibitedActionsMixin, DestroyMethodNotAllowedMixin, DjoserUserViewSet):
    queryset = User.objects.exclude_admin()
    filterset_class = UserFilter
    prohibited_actions = [
        ('put', 'update'),
        ('patch', 'partial_update'),
        ('delete', 'destroy')
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = super(UserViewSet, self).get_queryset()
        if self.action == 'list' and is_non_admin_user(user):
            queryset = queryset.exclude(id=user.id)
        return queryset

    def perform_destroy(self, instance):
        if getattr(settings, 'SEND_DELETE_CONFIRMATION', True):
            context = {"user": instance}
            to = [get_user_email(instance)]
            settings.EMAIL.delete(self.request, context).send(to)
        instance.delete()

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(user, User.USERNAME_FIELD, new_username)
        email_field_name = get_user_email_field_name(user)
        # deactivate user to reactivate it again throw email
        if User.USERNAME_FIELD == email_field_name:
            user.is_active = False
            # send deactivate signal
            signals.user_deactivated.send(
                sender=self.__class__, user=user, request=self.request
            )
        user.save()

        context = {"user": user}
        to = [get_user_email(user)]

        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)

        # send activation mail in case of being not activated, to guarantee that he owns this email
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            settings.EMAIL.activation(self.request, context).send(to)

        # logout after change the username field
        if settings.LOGOUT_ON_EMAIL_CHANGE:
            logout_user(self.request)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(serializer.user, User.USERNAME_FIELD, new_username)
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = timezone.now()

        user = serializer.user
        email_field_name = get_user_email_field_name(user)
        # deactivate user to reactivate it again throw email
        if User.USERNAME_FIELD == email_field_name:
            user.is_active = False
            # send deactivate signal
            signals.user_deactivated.send(
                sender=self.__class__, user=user, request=self.request
            )
        user.save()

        context = {"user": user}
        to = [get_user_email(user)]

        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)

        # send activation mail in case of being not activated, to guarantee that he owns this email
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            settings.EMAIL.activation(self.request, context).send(to)

        # logout after change the username field
        if settings.LOGOUT_ON_EMAIL_CHANGE:
            logout_user(self.request)

        return Response(status=status.HTTP_204_NO_CONTENT)
