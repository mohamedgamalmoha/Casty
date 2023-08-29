from django.urls import path, include

from rest_framework import routers

from .views import RateViewSet


app_name = 'reviews'

router = routers.DefaultRouter()
router.register(r'rates', RateViewSet, basename='rate')

urlpatterns = [
    path('', include(router.urls), name='review_rates'),
]
