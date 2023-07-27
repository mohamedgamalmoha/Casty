from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin

from rest_flex_fields import is_expanded
from drf_spectacular.utils import extend_schema

from profiles.models import Profile
from accounts.api.permissions import IsDirectorUser
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from agencies.models import Agency, PreviousWork, AgencyImage
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
        if self.action == 'me' and hasattr(user, 'agency'):
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
        return super(AgencyViewSet, self).get_permission_classes(request)

    def get_object(self):
        if self.action == 'me':
            return self.request.user.profile
        return super(AgencyViewSet, self).get_object()

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

    @extend_schema(request=None, responses={status.HTTP_200_OK: None, status.HTTP_204_NO_CONTENT: None,
                                            status.HTTP_405_METHOD_NOT_ALLOWED: None},
                   description="Follow / Unfollow other profiles\n"
                               "\t-200: The following is added successfully.\n"
                               "\t-204: The following is deleted successfully.\n"
                               "\t-405: Http method is not allowed.\n")
    @action(detail=True, methods=['POST', 'DELETE'], name='Follow Model', url_path='follow-model')
    def follow_model(self, request, pk=None):
        agency = request.user.agency
        following_profile = get_object_or_404(Profile, id=pk)
        if request.method == 'POST':
            agency.following_models.add(following_profile)
            return Response(status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            agency.following_models.remove(following_profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(request=None, responses={status.HTTP_200_OK: None, status.HTTP_204_NO_CONTENT: None,
                                            status.HTTP_405_METHOD_NOT_ALLOWED: None},
                   description="Follow / Unfollow other profiles\n"
                               "\t-200: The following is added successfully.\n"
                               "\t-204: The following is deleted successfully.\n"
                               "\t-400: The following is canceled cause the tow profiles were the same.\n"
                               "\t-405: Http method is not allowed.\n")
    @action(detail=True, methods=['POST', 'DELETE'], name='Follow Agency', url_path='follow-agency')
    def follow_agency(self, request, pk=None):
        agency = request.user.agency
        following_profile = self.get_object()
        if request.method == 'POST':
            agency.following_agencies.add(following_profile)
            return Response(status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            agency.following_agencies.remove(following_profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileImageViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, UpdateModelMixin, ListModelMixin,
                          DestroyModelMixin, GenericViewSet):
    queryset = AgencyImage.objects.filter(is_active=True)
    serializer_class = AgencyImageSerializer
    permission_classes = [IsDirectorUser]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and hasattr(user, 'agency'):
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
