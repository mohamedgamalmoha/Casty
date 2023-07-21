from django.db import models

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from rest_flex_fields import is_expanded
from drf_spectacular.utils import extend_schema

from accounts.api.permissions import IsDirectorUser
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from agencies.models import Agency, PreviousWork
from .filters import AgencyFilter, PreviousWorkFilter
from .serializers import AgencySerializer, PreviousWorkSerializer


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
