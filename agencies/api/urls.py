from django.urls import path, include

from rest_framework import routers

from .views import AgencyViewSet, PreviousWorkViewSet, AgencyImageViewSet


app_name = 'agencies'

router = routers.DefaultRouter()
router.register(r'agency', AgencyViewSet, basename='agency')
router.register(r'prev-work', PreviousWorkViewSet, basename='work')
router.register(r'images', AgencyImageViewSet, basename='images')

urlpatterns = [
    path('', include(router.urls), name='profile_routes'),
]
