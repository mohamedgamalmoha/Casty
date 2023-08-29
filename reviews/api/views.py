from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin

from drf_spectacular.utils import extend_schema

from reviews.models import Rate
from accounts.utils import is_model_user, is_director_user
from accounts.api.permissions import IsModelUser, IsDirectorUser
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from .serializers import RateSerializer


class RateViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                  GenericViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsDirectorUser]
    save_method_permission_classes = [IsModelUser | IsDirectorUser]

    def method_not_allowed(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Pass the view set action & pk to the serializer context
        context['action'] = self.action
        context['pk'] = self.kwargs.get('pk')
        return context

    def perform_create(self, serializer):
        serializer.save(agency=self.request.user.agency)

    @extend_schema(responses={200: RateSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='my-reviews', url_path='my-reviews')
    def my_reviews(self, request, *args, **kwargs):
        user = request.user

        if is_model_user(user):
            self.queryset = self.queryset.filter(profile=user.profile)

        if is_director_user(user):
            self.queryset = self.queryset.filter(agency=user.agency)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=None, responses={status.HTTP_405_METHOD_NOT_ALLOWED: None})
    def create(self, request, *args, **kwargs):
        if self.action == 'create':
            return self.method_not_allowed(request, *args, **kwargs)
        return super().create(request, *args, **kwargs)

    @extend_schema(responses={200: RateSerializer()})
    @action(detail=True, methods=["POST"], name='contract-request', url_path='contract-request')
    def contract_request(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: RateSerializer()})
    @action(detail=True, methods=["POST"], name='solo-contract', url_path='solo-contract')
    def solo_contract(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
