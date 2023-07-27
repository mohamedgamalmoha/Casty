from django.urls import path, include

from rest_framework import routers

from .views import (SkillViewSet, LanguageViewSet, ProfileViewSet, SocialLinkViewSet, PreviousExperienceViewSet,
                    ProfileImageViewSet)


app_name = 'profile'

router = routers.DefaultRouter()
router.register(r'skill', SkillViewSet, basename='skill')
router.register(r'language', LanguageViewSet, basename='language')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'social-link', SocialLinkViewSet, basename='social_link')
router.register(r'prev-exp', PreviousExperienceViewSet, basename='prev_exp')
router.register(r'images', ProfileImageViewSet, basename='images')

urlpatterns = [
    path('', include(router.urls), name='profile_routes'),
]
