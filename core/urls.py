"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,
                                   SpectacularJSONAPIView)

from accounts.sites import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    # API Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/json/', SpectacularJSONAPIView.as_view(), name='spec_json'),

    # Custom Apps
    path('api/', include('accounts.api.urls', namespace='accounts')),
    path('api/', include('profiles.api.urls', namespace='profiles')),
    path('api/', include('agencies.api.urls', namespace='agencies')),
    path('api/', include('reports.api.urls', namespace='reports')),
    path('api/', include('contracts.api.urls', namespace='contracts')),
    path('api/', include('info.api.urls', namespace='info')),
    path('api/', include('reviews.api.urls', namespace='reviews')),
    path('api/', include('stats.api.urls', namespace='stats')),

    # Custom Views
    path('account/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
