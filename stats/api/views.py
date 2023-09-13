from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.contrib.auth.backends import get_user_model

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser

from drf_spectacular.utils import extend_schema

from reviews.models import Rate
from reports.models import Report
from contracts.models import Contract, SoloContract
from .pagination import StatsPageNumberPagination
from .filters import (UserStatsFilter, ReportStatsFilter, RateStatsFilter, ContractStatsFilter, SoloContractStatsFilter)
from .serializers import (DateCountUserStatsSerializer, RoleCountUserStatsSerializer, DateCountReportStatsSerializer,
                          TypeCountReportStatsSerializer, DateCountRateStatsSerializer, RateCountRateStatsSerializer,
                          DateSumRateStatsSerializer, DateCountContractStatsSerializer, DateSumContractStatsSerializer,
                          DateCountSoloContractStatsSerializer, DateSumSoloContractStatsSerializer)


User = get_user_model()


class UserStatsViewSet(GenericViewSet):
    queryset = User.objects.exclude_admin()
    filterset_class = UserStatsFilter
    permission_classes = [IsAdminUser]
    pagination_class = StatsPageNumberPagination
    list_view = ListModelMixin.list

    def get_serializer_class(self):
        if self.action == 'daily_count':
            return DateCountUserStatsSerializer
        if self.action == 'role_count':
            return RoleCountUserStatsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'daily_count':
            return queryset.annotate(
                date=TruncDate('date_joined')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('-date')
        if self.action == 'role_count':
            return queryset.values('role').annotate(
                count=Count('id')
            ).order_by('count')
        return queryset

    @extend_schema(responses={200: DateCountUserStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: RoleCountUserStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='role-count')
    def role_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)


class ReportStatsViewSet(GenericViewSet):
    queryset = Report.objects.all()
    filterset_class = ReportStatsFilter
    permission_classes = [IsAdminUser]
    pagination_class = StatsPageNumberPagination
    list_view = ListModelMixin.list

    def get_serializer_class(self):
        if self.action == 'daily_count':
            return DateCountReportStatsSerializer
        if self.action == 'type_count':
            return TypeCountReportStatsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'daily_count':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('-date')
        if self.action == 'type_count':
            return queryset.values('type').annotate(
                count=Count('id')
            ).order_by('count')
        return queryset

    @extend_schema(responses={200: DateCountReportStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: TypeCountReportStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='type-count')
    def type_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)


class RateStatsViewSet(GenericViewSet):
    queryset = Rate.objects.all()
    filterset_class = RateStatsFilter
    permission_classes = [IsAdminUser]
    pagination_class = StatsPageNumberPagination
    list_view = ListModelMixin.list

    def get_serializer_class(self):
        if self.action == 'daily_count':
            return DateCountRateStatsSerializer
        if self.action == 'daily_sum':
            return DateSumRateStatsSerializer
        if self.action == 'rate_count':
            return RateCountRateStatsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'daily_count':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('-date')
        if self.action == 'daily_sum':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                sum=Sum('rate')
            ).order_by('-date')
        if self.action == 'rate_count':
            return queryset.values('rate').annotate(
                count=Count('id')
            ).order_by('count')
        return queryset

    @extend_schema(responses={200: DateCountRateStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: DateSumRateStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-sum')
    def daily_sum(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: RateCountRateStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='rate-count')
    def rate_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)


class ContractStatsViewSet(GenericViewSet):
    queryset = Contract.objects.all()
    filterset_class = ContractStatsFilter
    permission_classes = [IsAdminUser]
    pagination_class = StatsPageNumberPagination
    list_view = ListModelMixin.list

    def get_serializer_class(self):
        if self.action == 'daily_count':
            return DateCountContractStatsSerializer
        if self.action == 'offer_sum':
            return DateSumContractStatsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'daily_count':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('-date')
        if self.action == 'offer_sum':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                sum=Sum('money_offer')
            ).order_by('-date')
        return queryset

    @extend_schema(responses={200: DateCountContractStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: DateSumContractStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='offer-sum')
    def offer_sum(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)


class SoloContractStatsViewSet(GenericViewSet):
    queryset = SoloContract.objects.all()
    filterset_class = SoloContractStatsFilter
    permission_classes = [IsAdminUser]
    pagination_class = StatsPageNumberPagination
    list_view = ListModelMixin.list

    def get_serializer_class(self):
        if self.action == 'daily_count':
            return DateCountSoloContractStatsSerializer
        if self.action == 'offer_sum':
            return DateSumSoloContractStatsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'daily_count':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('-date')
        if self.action == 'offer_sum':
            return queryset.annotate(
                date=TruncDate('create_at')
            ).values('date').annotate(
                sum=Sum('money_offer')
            ).order_by('-date')
        return queryset

    @extend_schema(responses={200: DateCountSoloContractStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='daily-count')
    def daily_count(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)

    @extend_schema(responses={200: DateSumSoloContractStatsSerializer(many=True)})
    @action(["GET"], detail=False, url_path='offer-sum')
    def offer_sum(self, request, *args, **kwargs):
        return self.list_view(request, *args, **kwargs)
