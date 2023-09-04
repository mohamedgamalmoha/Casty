from modeltranslation.translator import translator, TranslationOptions

from .models import MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, HeaderImage, TeamMember


class MainInfoTranslationOptions(TranslationOptions):
    fields = ('why_us', )


class FAQsTranslationOptions(TranslationOptions):
    fields = ('quote', 'answer')


class TitledDescriptiveTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class HeaderImageTranslationOptions(TranslationOptions):
    fields = ('alt', )


class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('name', "position", "about")


translator.register(FAQs, FAQsTranslationOptions)
translator.register(MainInfo, MainInfoTranslationOptions)
translator.register(HeaderImage, HeaderImageTranslationOptions)
translator.register(AboutUs, TitledDescriptiveTranslationOptions)
translator.register(CookiePolicy, TitledDescriptiveTranslationOptions)
translator.register(PrivacyPolicy, TitledDescriptiveTranslationOptions)
translator.register(TermsOfService, TitledDescriptiveTranslationOptions)
translator.register(TeamMember, TeamMemberTranslationOptions)
