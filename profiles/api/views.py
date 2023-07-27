from django.db import models

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin

from rest_flex_fields import is_expanded
from drf_spectacular.utils import extend_schema

from accounts.api.permissions import IsModelUser
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from profiles.models import Skill, Language, Profile, SocialLink, PreviousExperience, ProfileImage
from .filters import ProfileFilter, PreviousExperienceFilter
from .serializers import (SkillSerializer, LanguageSerializer, ProfileSerializer, SocialLinkSerializer,
                          PreviousExperienceSerializer, ProfileImageSerializer)


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
    permission_classes = [IsModelUser]
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
    permission_classes = [IsModelUser]
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
    permission_classes = [IsModelUser]
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
        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related(
                models.Prefetch('images', queryset=ProfileImage.objects.filter(is_active=True))
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

    @extend_schema(request=None, responses={status.HTTP_200_OK: None, status.HTTP_204_NO_CONTENT: None,
                                            status.HTTP_405_METHOD_NOT_ALLOWED: None},
                   description="Follow / Unfollow other profiles\n"
                               "\t-200: The following is added successfully.\n"
                               "\t-204: The following is deleted successfully.\n"
                               "\t-400: The following is canceled cause the tow profiles were the same.\n"
                               "\t-405: Http method is not allowed.\n")
    @action(detail=True, methods=['POST', 'DELETE'], name='follow')
    def follow(self, request, pk=None):
        profile = request.user.profile
        following_profile = self.get_object()
        if profile == following_profile:
            return Response({'error': 'Follow your own profile is not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            profile.following.add(following_profile)
            return Response(status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            profile.following.remove(following_profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProfileImageViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, UpdateModelMixin, ListModelMixin,
                          DestroyModelMixin, GenericViewSet):
    queryset = ProfileImage.objects.filter(is_active=True)
    serializer_class = ProfileImageSerializer
    permission_classes = [IsModelUser]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and hasattr(user, 'profile'):
            queryset = queryset.filter(profile=user.profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @extend_schema(responses={200: ProfileImageSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='Get My Images')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
