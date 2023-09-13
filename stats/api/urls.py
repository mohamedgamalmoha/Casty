from django.urls import path, include

from rest_framework import routers

from .views import (UserStatsViewSet, ReportStatsViewSet, RateStatsViewSet, ContractStatsViewSet,
                    SoloContractStatsViewSet)


app_name = 'stats'

router = routers.DefaultRouter()
router.register('users', UserStatsViewSet, basename='users')
router.register('reports', ReportStatsViewSet, basename='reports')
router.register('rates', RateStatsViewSet, basename='rates')
router.register('contracts', ContractStatsViewSet, basename='contracts')
router.register('solo-contracts', SoloContractStatsViewSet, basename='solo_contracts')

urlpatterns = [
    path('stats/', include(router.urls), name='users'),
]
