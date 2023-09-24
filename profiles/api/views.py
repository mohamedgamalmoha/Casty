from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin

from rest_flex_fields import is_expanded
from rest_flex_fields.filter_backends import FlexFieldsDocsFilterBackend
from drf_spectacular.utils import extend_schema

from accounts.api.permissions import IsModelUser, IsDirectorUser
from accounts.utils import is_model_user, is_owner, get_user_associated_model
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin, ProhibitedActionsMixin
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
        if self.action == 'me' and is_model_user(user):
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
        if self.action == 'me' and is_model_user(user):
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


class ProfileViewSet(ProhibitedActionsMixin, AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin,
                     UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsModelUser]
    filter_backends = GenericViewSet.filter_backends + [FlexFieldsDocsFilterBackend]
    save_method_permission_classes = [IsAuthenticated]
    follow_permission_classes = [IsModelUser | IsDirectorUser]
    prohibited_actions = [
        ('put', 'update'),
        ('patch', 'partial_update'),
    ]

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
        if self.action in ('follow', 'unfollow', 'followers', 'my_followers'):
            return self.follow_permission_classes
        return super().get_permission_classes(request)

    def get_object(self):
        if self.action == 'me':
            return self.request.user.profile
        return super(ProfileViewSet, self).get_object()

    def get_user_associated_model_or_403(self):
        user = self.request.user
        account = get_user_associated_model(user)
        if account is None:
            raise PermissionDenied()
        return account

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

    @extend_schema(request=None, responses={status.HTTP_200_OK: None, status.HTTP_400_BAD_REQUEST: None},
                   description="Follow / Unfollow other profiles\n"
                               "\t-200: The following is added successfully.\n"
                               "\t-400: The following is canceled cause the tow profiles were the same.\n")
    @action(detail=True, methods=['POST'], name='Follow Model', url_path='follow')
    def follow(self, request, pk=None):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_user_associated_model_or_403()
        # Check if the user has the same profile as target
        following_profile = self.get_object()
        if is_owner(request.user, following_profile):
            return Response({'error': _('Follow your own profile is not allowed')}, status=status.HTTP_400_BAD_REQUEST)
        # Add the target to profile
        account.following_models.add(following_profile)
        return Response(status=status.HTTP_200_OK)

    @extend_schema(request=None, responses={status.HTTP_204_NO_CONTENT: None},
                   description="UnFollow Model\n"
                               "\t-204: The following is deleted successfully.\n")
    @action(detail=True, methods=['POST'], name='Unfollow Model', url_path='unfollow')
    def unfollow(self, request, pk=None):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_user_associated_model_or_403()
        # Get the target profile
        following_profile = self.get_object()
        # Remove the target from followers
        account.following_models.remove(following_profile)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None, responses={status.HTTP_200_OK: ProfileSerializer(many=True),
                                            status.HTTP_403_FORBIDDEN: None})
    @action(detail=False, methods=['GET'], name='Get My Followers', url_path='my-followers')
    def my_followers(self, request, *args, **kwargs):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_user_associated_model_or_403()
        # Assign user followers as queryset
        self.queryset = account.following_models.all()
        return self.list(request, *args, **kwargs)

    @extend_schema(request=None, responses={status.HTTP_200_OK: ProfileSerializer(many=True),
                                            status.HTTP_403_FORBIDDEN: None})
    @action(detail=True, methods=['GET'], name='Get Followers', url_path='followers')
    def followers(self, request, *args, **kwargs):
        # Check the type of the user, in case of not being model or director, an exception is thrown
        account = self.get_object()
        # Assign user followers as queryset
        self.queryset = account.following_models.all()
        return self.list(request, *args, **kwargs)


class ProfileImageViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, UpdateModelMixin, ListModelMixin,
                          DestroyModelMixin, GenericViewSet):
    queryset = ProfileImage.objects.filter(is_active=True)
    serializer_class = ProfileImageSerializer
    permission_classes = [IsModelUser]
    save_method_permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and is_model_user(user):
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
