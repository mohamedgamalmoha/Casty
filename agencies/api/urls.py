from django.urls import path, include

from rest_framework import routers

from .views import AgencyViewSet, PreviousWorkViewSet


app_name = 'agencies'

router = routers.DefaultRouter()
router.register(r'agency', AgencyViewSet, basename='agency')
router.register(r'prev-work', PreviousWorkViewSet, basename='work')

urlpatterns = [
    path('', include(router.urls), name='profile_routes'),
]
