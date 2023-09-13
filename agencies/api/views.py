from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin

from rest_flex_fields import is_expanded
from drf_spectacular.utils import extend_schema

from agencies.models import Agency, PreviousWork, AgencyImage
from accounts.api.permissions import IsDirectorUser, IsModelUser
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from accounts.utils import is_director_user, is_owner, get_user_associated_model
from .filters import AgencyFilter, PreviousWorkFilter
from .serializers import AgencySerializer, PreviousWorkSerializer, AgencyImageSerializer


class PreviousWorkViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, ModelViewSet):
    queryset = PreviousWork.objects.all()
    serializer_class = PreviousWorkSerializer
    filterset_class = PreviousWorkFilter
    permission_classes = [IsDirectorUser]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and is_director_user(user):
            queryset = queryset.filter(profile=user.agency)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.agency)

    @extend_schema(responses={200: PreviousWorkSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='Get My Previous Works')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AgencyViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                    GenericViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    filterset_class = AgencyFilter
    permission_classes = [IsDirectorUser]
    save_method_permission_classes = [IsAuthenticated]
    follow_permission_classes = [IsModelUser | IsDirectorUser]

    def get_queryset(self):
        queryset = super(AgencyViewSet, self).get_queryset()
        if is_expanded(self.request, 'works'):
            queryset = queryset.prefetch_related(
                models.Prefetch('works', queryset=PreviousWork.objects.filter(is_active=True))
            )
        return queryset

    def get_permission_classes(self, request):
        if self.action == 'me':
            return self.permission_classes
        if self.action in ('follow', 'unfollow', 'followers', 'my_followers'):
            return self.follow_permission_classes
        return super(AgencyViewSet, self).get_permission_classes(request)

    def get_object(self):
        if self.action == 'me':
            return self.request.user.profile
        return super(AgencyViewSet, self).get_object()

    def get_user_associated_model_or_403(self):
        user = self.request.user
        account = get_user_associated_model(user)
        if account is None:
            raise PermissionDenied()
        return account

    @extend_schema(responses={200: AgencySerializer})
    @action(detail=False, methods=["GET", "PUT", "PATCH"], name='Get My Agency')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(request=None, responses={status.HTTP_200_OK: None, status.HTTP_400_BAD_REQUEST: None},
                   description="Follow Agency\n"
                               "\t-200: The following is added successfully.\n"
                               "\t-204: The following is deleted successfully.\n")
    @action(detail=True, methods=['POST'], name='Follow Agency', url_path='follow')
    def follow(self, request, pk=None):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_user_associated_model_or_403()
        # Check if the user has the same profile as target
        following_agency = self.get_object()
        if is_owner(request.user, following_agency):
            return Response({'error': _('Follow your own agency is not allowed')}, status=status.HTTP_400_BAD_REQUEST)
        account.following_agencies.add(following_agency)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(request=None, responses={status.HTTP_204_NO_CONTENT: None},
                   description="UnFollow Agency\n"
                               "\t-204: The following is deleted successfully.\n")
    @action(detail=True, methods=['POST'], name='Unfollow Model', url_path='unfollow')
    def unfollow(self, request, pk=None):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_user_associated_model_or_403()
        # Get the target profile
        following_agency = self.get_object()
        # Remove the target from followers
        account.following_agencies.remove(following_agency)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None, responses={status.HTTP_200_OK: AgencySerializer(many=True),
                                            status.HTTP_403_FORBIDDEN: None})
    @action(detail=False, methods=['GET'], name='Get My Followers', url_path='my-followers')
    def my_followers(self, request, *args, **kwargs):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_user_associated_model_or_403()
        # Assign user followers as queryset
        self.queryset = account.following_models.all()
        return self.list(request, *args, **kwargs)

    @extend_schema(request=None, responses={status.HTTP_200_OK: AgencySerializer(many=True),
                                            status.HTTP_403_FORBIDDEN: None})
    @action(detail=True, methods=['GET'], name='Get Followers', url_path='followers')
    def followers(self, request, *args, **kwargs):
        # Get the target
        account = self.get_object()
        # Assign target followers as queryset
        self.queryset = account.following_models.all()
        return self.list(request, *args, **kwargs)


class AgencyImageViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, UpdateModelMixin, ListModelMixin,
                         DestroyModelMixin, GenericViewSet):
    queryset = AgencyImage.objects.filter(is_active=True)
    serializer_class = AgencyImageSerializer
    permission_classes = [IsDirectorUser]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and is_director_user(user):
            queryset = queryset.filter(agency=user.agency)
        return queryset

    def perform_create(self, serializer):
        serializer.save(agency=self.request.user.agency)

    @extend_schema(responses={200: AgencyImageSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='Get My Images')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
