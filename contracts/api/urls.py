from django.urls import path, include

from rest_framework import routers

from .views import ContractViewSet, ContractRequestViewSet, SoloContractViewSet


app_name = 'contracts'

router = routers.DefaultRouter()
router.register(r'contract', ContractViewSet, basename='contract')
router.register(r'contract-request', ContractRequestViewSet, basename='contract-request')
router.register(r'contract-solo', SoloContractViewSet, basename='contract-solo')

urlpatterns = [
    path('', include(router.urls), name='profile_routes'),
]
