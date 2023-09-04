from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView


from info.models import MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, HeaderImage, TeamMember
from .mixins import TranslationViewMixin
from .filters import (FAQsFilter, AboutUsFilter, TermsOfServiceFilter, CookiePolicyFilter, PrivacyPolicyFilter,
                      TeamMemberFilter)
from .serializers import (MainInfoSerializer, FAQsSerializer, AboutUsSerializer, TermsOfServiceSerializer,
                          CookiePolicySerializer, PrivacyPolicySerializer, ContactUsSerializer, HeaderImageSerializer,
                          TeamMemberSerializer)


class MainInfoAPIView(TranslationViewMixin, RetrieveAPIView):
    queryset = MainInfo.objects.all()
    serializer_class = MainInfoSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.get_queryset().first()


class FAQsAPIView(TranslationViewMixin, ListAPIView):
    queryset = FAQs.objects.all()
    serializer_class = FAQsSerializer
    filterset_class = FAQsFilter
    permission_classes = [AllowAny]


class AboutUsAPIView(TranslationViewMixin, ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    filterset_class = AboutUsFilter
    permission_classes = [AllowAny]


class TermsOfServiceAPIView(TranslationViewMixin, ListAPIView):
    queryset = TermsOfService.objects.all()
    serializer_class = TermsOfServiceSerializer
    filterset_class = TermsOfServiceFilter
    permission_classes = [AllowAny]


class CookiePolicyAPIView(TranslationViewMixin, ListAPIView):
    queryset = CookiePolicy.objects.all()
    serializer_class = CookiePolicySerializer
    filterset_class = CookiePolicyFilter
    permission_classes = [AllowAny]


class PrivacyPolicyAPIView(TranslationViewMixin, ListAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    filterset_class = PrivacyPolicyFilter
    permission_classes = [AllowAny]


class ContactUsAPIView(CreateAPIView):
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]


class HeaderImageAPIView(TranslationViewMixin, ListAPIView):
    queryset = HeaderImage.objects.active()
    serializer_class = HeaderImageSerializer
    permission_classes = [AllowAny]


class TeamMemberAPIView(ListAPIView):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    filterset_class = TeamMemberFilter
    permission_classes = [AllowAny]
