from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema

from reports.models import Report, ReportResponse
from accounts.api.permissions import IsModelUser, IsDirectorUser
from .filters import ReportFilter
from .serializers import ReportSerializer, ReportResponseSerializer


User = get_user_model()


class ReportViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filterset_class = ReportFilter
    permission_classes = [IsModelUser | IsDirectorUser]
    action_map = {'list': 'my_reports'}

    def method_not_allowed(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_context(self):
        context = super(ReportViewSet, self).get_serializer_context()
        # Pass the view set action & pk to the serializer context
        context['action'] = self.action
        context['pk'] = self.kwargs.get('pk')
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(responses={200: ReportSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='my-reports', url_path='my-reports')
    def my_reports(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
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
        return super(ReportViewSet, self).create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='profile', url_path='profile')
    def profile(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='social-link', url_path='social-link')
    def social_link(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='previous-experience', url_path='previous-experience')
    def previous_experience(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='profile-image', url_path='profile-image')
    def profile_image(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='agency', url_path='agency')
    def agency(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='previous-work', url_path='previous-work')
    def previous_work(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(responses={200: ReportSerializer()})
    @action(detail=True, methods=["POST"], name='agency-image', url_path='agency-image')
    def agency_image(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReportResponseViewSet(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = ReportResponse.objects.all()
    serializer_class = ReportResponseSerializer
    permission_classes = [IsModelUser | IsDirectorUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
