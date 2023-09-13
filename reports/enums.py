from django.db import models
from django.utils.translation import gettext_lazy as _


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class ReportTypeChoices(models.IntegerChoices):
    BUG_REPORT = 1, _('Bug Report')
    PERFORMANCE_ISSUE = 2, _('Performance Issue')
    UI_ISSUE = 3, _('User Interface (UI) Issue')
    SECURITY_VULNERABILITY = 4, _('Security Vulnerability')
    COMPATIBILITY_ISSUE = 5, _('Compatibility Issue')
    DATA_INTEGRITY_ISSUE = 6, _('Data Integrity Issue')
    DOCUMENTATION_ISSUE = 7, _('Documentation Issue')
    ACCESSIBILITY_ISSUE = 8, _('Accessibility Issue')
    HARDWARE_PROBLEM = 9, _('Hardware Problem')
    NETWORK_CONNECTIVITY_ISSUE = 10, _('Network Connectivity Issue')
    CRASH_REPORT = 11, _('Crash Report')
    INSTALLATION_DEPLOYMENT_ISSUE = 12, _('Installation/Deployment Issue')
    USABILITY_UX_ISSUE = 13, _('Usability/UX Issue')
    PERFORMANCE_DEGRADATION = 14, _('Performance Degradation')
    FEATURE_REQUEST = 15, _('Feature Request')
    DISCRIMINATION = 16, _('Discrimination')
    BULLYING = 17, _('Bullying')
    POVERTY_HOMELESSNESS = 18, _('Poverty and Homelessness')
    SUBSTANCE_ABUSE = 19, _('Substance Abuse')
    MENTAL_HEALTH_ISSUES = 20, _('Mental Health Issues')
    DOMESTIC_VIOLENCE = 21, _('Domestic Violence')
    HUMAN_TRAFFICKING = 22, _('Human Trafficking')
    ENVIRONMENTAL_CONCERNS = 23, _('Environmental Concerns')
    EDUCATION_DISPARITIES = 24, _('Education Disparities')
    HEALTHCARE_ACCESS = 25, _('Healthcare Access')
    GENDER_INEQUALITY = 26, _('Gender Inequality')
    RACIAL_INJUSTICE = 27, _('Racial Injustice')
    IMMIGRATION_REFUGEE_CHALLENGES = 28, _('Immigration and Refugee Challenges')
    CHILD_ABUSE_AND_NEGLECT = 29, _('Child Abuse and Neglect')
    PRIVACY_CONCERNS = 30, _('Privacy Concerns')
    NUDITY_CONTENT = 31, _('Nudity Content')
    OTHER = 32, _('Other')

    @classproperty
    def performance_based_choices(cls):
        return tuple(filter(lambda choice: 16 > choice[0], cls.choices))

    @classproperty
    def content_based_choices(cls):
        return tuple(filter(lambda choice: 32 > choice[0] > 15, cls.choices))


class ReportResponseChoices(models.IntegerChoices):
    ACKNOWLEDGE_EMPATHY = 1, _('Thank you for bringing this to our attention')
    ASSURANCE = 2, _('Rest assured, we\'re here to help you resolve this')
    IMMEDIATE_STEPS = 3, _('Let\'s start by troubleshooting the problem together')
    CLARIFICATION_INFO = 4, _('Could you please provide more details about the issue')
    RESOLUTION_TIMELINE = 5, _('We\'re working on a solution and aim to have this resolved as soon as possible')
    ALTERNATIVE_ASSISTANCE = 6, _('While we work on a solution, is there anything else we can help you with')
    FEEDBACK_IMPROVEMENT = 7, _('Your feedback is important to us and helps us improve our products/services')
    FOLLOW_UP = 8, _('Feel free to reach out if you have any questions or need further assistance')
    CLOSING = 9, _('Thank you for your patience and understanding as we resolve this')


def get_type_label_from_value(value):
    TypeDict = dict(ReportTypeChoices.choices)
    return TypeDict.get(value)
