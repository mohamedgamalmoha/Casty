from django.urls import path, include

from rest_framework import routers

from .views import ReportViewSet


app_name = 'reports'

router = routers.DefaultRouter()
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls), name='profile_routes'),
]
