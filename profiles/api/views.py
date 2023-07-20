from django.db import models

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from rest_flex_fields import is_expanded
from drf_spectacular.utils import extend_schema

from accounts.api.permissions import IsUserWithProfile
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from profiles.models import Skill, Language, Profile, SocialLink, PreviousExperience
from .filters import ProfileFilter, PreviousExperienceFilter
from .serializers import (SkillSerializer, LanguageSerializer, ProfileSerializer, SocialLinkSerializer,
                          PreviousExperienceSerializer)


class SkillViewSet(ReadOnlyModelViewSet):
    queryset = Skill.objects.filter(is_active=True)
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class LanguageViewSet(ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]


class SocialLinkViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsUserWithProfile]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and hasattr(user, 'profile'):
            queryset = queryset.filter(profile=user.profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @extend_schema(responses={200: SocialLinkSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='Get My Social Links')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PreviousExperienceViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, ModelViewSet):
    queryset = PreviousExperience.objects.all()
    serializer_class = PreviousExperienceSerializer
    filterset_class = PreviousExperienceFilter
    permission_classes = [IsUserWithProfile]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and hasattr(user, 'profile'):
            queryset = queryset.filter(profile=user.profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @extend_schema(responses={200: PreviousExperienceSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='Get My Previous Experiences')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsUserWithProfile]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_expanded(self.request, 'links'):
            queryset = queryset.prefetch_related(
                models.Prefetch('links', queryset=SocialLink.objects.filter(is_active=True))
            )
        if is_expanded(self.request, 'experiences'):
            queryset = queryset.prefetch_related(
                models.Prefetch('experiences', queryset=PreviousExperience.objects.filter(is_active=True))
            )
        return queryset

    def get_permission_classes(self, request):
        if self.action == 'me':
            return self.permission_classes
        return super().get_permission_classes(request)

    def get_object(self):
        if self.action == 'me':
            return self.request.user.profile
        return super(ProfileViewSet, self).get_object()

    @extend_schema(responses={200: ProfileSerializer})
    @action(detail=False, methods=["GET", "PUT", "PATCH"], name='Get My Profile')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
