from django.urls import path, re_path, include

from rest_framework import routers
from djoser.social.views import ProviderAuthView

from .views import UserViewSet


app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'auth/users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('djoser.urls.jwt'), name='jwt'),
    # re_path(r"^auth/social/(?P<provider>\S+)/$", ProviderAuthView.as_view(), name="social-auth-provider"),
    path('', include(router.urls), name='routes'),
]
