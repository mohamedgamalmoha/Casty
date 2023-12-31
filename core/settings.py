"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

import environ
from rest_framework import ISO_8601
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment variables
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(env('DEBUG'))

ALLOWED_HOSTS = [
    *env('ALLOWED_HOSTS').split(',')
]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'corsheaders',
    'django_middleware_global_request',
    "rest_framework",
    'djoser',
    'social_django',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'drf_spectacular',
    'djmoney',

    # Custom apps
    'accounts',
    'profiles',
    'agencies',
    'reports',
    'contracts',
    'info',
    'reviews',
    'stats'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_middleware_global_request.middleware.GlobalRequestMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# RestAPI Settings
REST_FRAMEWORK = {
    # Base API policies
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': None,

    # Generic view behavior
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],

    # Schema
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Throttling
    'DEFAULT_THROTTLE_RATES': {
        'user': None,
        'anon': None,
    },
    'NUM_PROXIES': None,

    # Pagination
    'PAGE_SIZE': 20,

    # Filtering
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',

    # Versioning
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',

    # Authentication
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    'UNAUTHENTICATED_TOKEN': None,

    # View configuration
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',
    # Exception handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',

    # Testing
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',

    # Hyperlink settings
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',

    # Input and output formats
    'DATE_FORMAT': ISO_8601,
    'DATE_INPUT_FORMATS': [ISO_8601],

    'DATETIME_FORMAT': ISO_8601,
    'DATETIME_INPUT_FORMATS': [ISO_8601],

    'TIME_FORMAT': ISO_8601,
    'TIME_INPUT_FORMATS': [ISO_8601],

    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,

    # Browseable API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",

    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}


# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("JWT",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# DJOSER Settings
DJOSER = {
    'PERMISSIONS': {
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
        'user_delete': ['accounts.api.permissions.DenyDelete'],
        "activation": ["rest_framework.permissions.AllowAny"],
        "password_reset": ["rest_framework.permissions.AllowAny"],
        "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
        "username_reset": ["rest_framework.permissions.AllowAny"],
        "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_username": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "token_create": ["rest_framework.permissions.AllowAny"],
    },
    'SERIALIZERS': {
        'activation': 'djoser.serializers.ActivationSerializer',
        'password_reset': 'djoser.serializers.SendEmailResetSerializer',
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
        'password_reset_confirm_retype': 'djoser.serializers.PasswordResetConfirmRetypeSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer',
        'set_password_retype': 'djoser.serializers.SetPasswordRetypeSerializer',
        'set_username': 'djoser.serializers.SetUsernameSerializer',
        'set_username_retype': 'djoser.serializers.SetUsernameRetypeSerializer',
        'username_reset': 'djoser.serializers.SendEmailResetSerializer',
        'username_reset_confirm': 'djoser.serializers.UsernameResetConfirmSerializer',
        'username_reset_confirm_retype': 'djoser.serializers.UsernameResetConfirmRetypeSerializer',
        'user_create': 'accounts.api.serializers.CustomUserCreateSerializer',
        'user_create_password_retype': 'djoser.serializers.UserCreatePasswordRetypeSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'user': 'accounts.api.serializers.CustomUserSerializer',
        'current_user': 'accounts.api.serializers.CustomUserSerializer',
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    "EMAIL": {
        "activation": "accounts.mail.CustomActivationEmail",
        "confirmation": "accounts.email.CustomConfirmationEmail",
        "password_reset": "accounts.email.CustomPasswordResetEmail",
        "password_changed_confirmation": "accounts.email.CustomPasswordChangedConfirmationEmail",
        "username_changed_confirmation": "accounts.email.CustomUsernameChangedConfirmationEmail",
        "username_reset": "accounts.email.CustomUsernameResetEmail",
        "delete": "accounts.email.DeleteEmail"
    },
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "CONSTANTS": {"messages": "djoser.constants.Messages"},
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
    "USER_ID_FIELD": 'id',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': bool(env('SEND_ACTIVATION_EMAIL')),
    'SEND_CONFIRMATION_EMAIL': bool(env('SEND_CONFIRMATION_EMAIL')),
    'SET_PASSWORD_RETYPE': True,
    'USER_CREATE_PASSWORD_RETYPE': False,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    "PASSWORD_RESET_CONFIRM_RETYPE": False,
    "SET_USERNAME_RETYPE": False,
    "USERNAME_RESET_CONFIRM_RETYPE": False,
    "USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "SEND_DELETE_CONFIRMATION": True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION¶': bool(env('USERNAME_CHANGED_EMAIL_CONFIRMATION')),
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION¶': bool(env('USERNAME_CHANGED_EMAIL_CONFIRMATION')),
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['/google', '/facebook'],
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "LOGOUT_ON_EMAIL_CHANGE": True,
    "CREATE_SESSION_ON_LOGIN": False,
}


# Spectacular Settings
SPECTACULAR_SETTINGS = {
    # A regex specifying the common denominator for all operation paths. If
    # SCHEMA_PATH_PREFIX is set to None, drf-spectacular will attempt to estimate
    # a common prefix. Use '' to disable.
    # Mainly used for tag extraction, where paths like '/api/v1/albums' with
    # a SCHEMA_PATH_PREFIX regex '/api/v[0-9]' would yield the tag 'albums'.
    'SCHEMA_PATH_PREFIX': None,
    # Remove matching SCHEMA_PATH_PREFIX from operation path. Usually used in
    # conjunction with appended prefixes in SERVERS.
    'SCHEMA_PATH_PREFIX_TRIM': False,
    # Insert a manual path prefix to the operation path, e.g. '/service/backend'.
    # Use this for example to align paths when the API is mounted as a sub-resource
    # behind a proxy and Django is not aware of that. Alternatively, prefixes can
    # also specified via SERVERS, but this makes the operation path more explicit.
    'SCHEMA_PATH_PREFIX_INSERT': '',
    # Coercion of {pk} to {id} is controlled by SCHEMA_COERCE_PATH_PK. Additionally,
    # some libraries (e.g. drf-nested-routers) use "_pk" suffixed path variables.
    # This setting globally coerces path variables like "{user_pk}" to "{user_id}".
    'SCHEMA_COERCE_PATH_PK_SUFFIX': False,

    # Schema generation parameters to influence how components are constructed.
    # Some schema features might not translate well to your target.
    # Demultiplexing/modifying components might help alleviate those issues.
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    # Create separate components for PATCH endpoints (without required list)
    'COMPONENT_SPLIT_PATCH': True,
    # Split components into request and response parts where appropriate
    # This setting is highly recommended to achieve the most accurate API
    # description, however it comes at the cost of having more components.
    'COMPONENT_SPLIT_REQUEST': False,
    # Aid client generator targets that have trouble with read-only properties.
    'COMPONENT_NO_READ_ONLY_REQUIRED': False,

    # Adds "minLength: 1" to fields that do not allow blank strings. Deactivated
    # by default because serializers do not strictly enforce this on responses and
    # so "minLength: 1" may not always accurately describe API behavior.
    # Gets implicitly enabled by COMPONENT_SPLIT_REQUEST, because this can be
    # accurately modeled when request and response components are separated.
    'ENFORCE_NON_BLANK_FIELDS': False,

    # Configuration for serving a schema subset with SpectacularAPIView
    'SERVE_URLCONF': None,
    # complete public schema or a subset based on the requesting user
    'SERVE_PUBLIC': True,
    # include schema endpoint into schema
    'SERVE_INCLUDE_SCHEMA': True,
    # list of authentication/permission classes for spectacular's views.
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    # None will default to DRF's AUTHENTICATION_CLASSES
    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # Dictionary of general configuration to pass to the SwaggerUI({ ... })
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    # The settings are serialized with json.dumps(). If you need customized JS, use a
    # string instead. The string must then contain valid JS and is passed unchanged.
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
    },
    # Initialize SwaggerUI with additional OAuth2 configuration.
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/
    'SWAGGER_UI_OAUTH2_CONFIG': {},

    # Dictionary of general configuration to pass to the Redoc.init({ ... })
    # https://github.com/Redocly/redoc#redoc-options-object
    # The settings are serialized with json.dumps(). If you need customized JS, use a
    # string instead. The string must then contain valid JS and is passed unchanged.
    'REDOC_UI_SETTINGS': {},

    # CDNs for swagger and redoc. You can change the version or even host your
    # own depending on your requirements. For self-hosting, have a look at
    # the sidecar option in the README.
    'SWAGGER_UI_DIST': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest',
    'SWAGGER_UI_FAVICON_HREF': '/static/images/logo_favicon.png',
    'REDOC_DIST': 'https://cdn.jsdelivr.net/npm/redoc@latest',

    # Append OpenAPI objects to path and components in addition to the generated objects
    'APPEND_PATHS': {},
    'APPEND_COMPONENTS': {},

    # DISCOURAGED - please don't use this anymore as it has tricky implications that
    # are hard to get right. For authentication, OpenApiAuthenticationExtension are
    # strongly preferred because they are more robust and easy to write.
    # However if used, the list of methods is appended to every endpoint in the schema!
    'SECURITY': [],

    # Postprocessing functions that run at the end of schema generation.
    # must satisfy interface result = hook(generator, request, public, result)
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
        'core.hocks.postprocessing_exclude_stats_path'
    ],

    # Preprocessing functions that run before schema generation.
    # must satisfy interface result = hook(endpoints=result) where result
    # is a list of Tuples (path, path_regex, method, callback).
    # Example: 'drf_spectacular.hooks.preprocess_exclude_path_format'
    'PREPROCESSING_HOOKS': [],

    # Determines how operations should be sorted. If you intend to do sorting with a
    # PREPROCESSING_HOOKS, be sure to disable this setting. If configured, the sorting
    # is applied after the PREPROCESSING_HOOKS. Accepts either
    # True (drf-spectacular's alpha-sorter), False, or a callable for sort's key arg.
    'SORT_OPERATIONS': True,

    # enum name overrides. dict with keys "YourEnum" and their choice values "field.choices"
    # e.g. {'SomeEnum': ['A', 'B'], 'OtherEnum': 'import.path.to.choices'}
    'ENUM_NAME_OVERRIDES': {},
    # Adds "blank" and "null" enum choices where appropriate. disable on client generation issues
    'ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE': True,
    # Add/Append a list of (``choice value`` - choice name) to the enum description string.
    'ENUM_GENERATE_CHOICE_DESCRIPTION': True,

    # function that returns a list of all classes that should be excluded from doc string extraction
    'GET_LIB_DOC_EXCLUDES': 'drf_spectacular.plumbing.get_lib_doc_excludes',

    # Function that returns a mocked request for view processing. For CLI usage
    # original_request will be None.
    # interface: request = build_mock_request(method, path, view, original_request, **kwargs)
    'GET_MOCK_REQUEST': 'drf_spectacular.plumbing.build_mock_request',

    # Camelize names like "operationId" and path parameter names
    # Camelization of the operation schema itself requires the addition of
    # 'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields'
    # to POSTPROCESSING_HOOKS. Please note that the hook depends on
    # ``djangorestframework_camel_case``, while CAMELIZE_NAMES itself does not.
    'CAMELIZE_NAMES': False,

    # Determines if and how free-form 'additionalProperties' should be emitted in the schema. Some
    # code generator targets are sensitive to this. None disables generic 'additionalProperties'.
    # allowed values are 'dict', 'bool', None
    'GENERIC_ADDITIONAL_PROPERTIES': 'dict',

    # Path converter schema overrides (e.g. <int:foo>). Can be used to either modify default
    # behavior or provide a schema for custom converters registered with register_converter(...).
    # Takes converter labels as keys and either basic python types, OpenApiType, or raw schemas
    # as values. Example: {'aint': OpenApiTypes.INT, 'bint': str, 'cint': {'type': ...}}
    'PATH_CONVERTER_OVERRIDES': {},

    # Determines whether operation parameters should be sorted alphanumerically or just in
    # the order they arrived. Accepts either True, False, or a callable for sort's key arg.
    'SORT_OPERATION_PARAMETERS': True,

    # @extend_schema allows to specify status codes besides 200. This functionality is usually used
    # to describe error responses, which rarely make use of list mechanics. Therefore, we suppress
    # listing (pagination and filtering) on non-2XX status codes by default. Toggle this to enable
    # list responses with ListSerializers/many=True irrespective of the status code.
    'ENABLE_LIST_MECHANICS_ON_NON_2XX': False,

    # This setting allows you to deviate from the default manager by accessing a different model
    # property. We use "objects" by default for compatibility reasons. Using "_default_manager"
    # will likely fix most issues, though you are free to choose any name.
    "DEFAULT_QUERY_MANAGER": 'objects',

    # Controls which authentication methods are exposed in the schema. If not None, will hide
    # authentication classes that are not contained in the whitelist. Use full import paths
    # like ['rest_framework.authentication.TokenAuthentication', ...].
    # Empty list ([]) will hide all authentication methods. The default None will show all.
    'AUTHENTICATION_WHITELIST': None,
    # Controls which parsers are exposed in the schema. Works analog to AUTHENTICATION_WHITELIST.
    # List of allowed parsers or None to allow all.
    'PARSER_WHITELIST': None,
    # Controls which renderers are exposed in the schema. Works analog to AUTHENTICATION_WHITELIST.
    # rest_framework.renderers.BrowsableAPIRenderer is ignored by default if whitelist is None
    'RENDERER_WHITELIST': None,

    # Option for turning off error and warn messages
    'DISABLE_ERRORS_AND_WARNINGS': True,

    # Runs exemplary schema generation and emits warnings as part of "./manage.py check --deploy"
    'ENABLE_DJANGO_DEPLOY_CHECK': True,

    # General schema metadata. Refer to spec for valid inputs
    # https://spec.openapis.org/oas/v3.0.3#openapi-object
    'TITLE': 'Casty',
    'DESCRIPTION': 'Casty API Endpoints',
    'TOS': None,
    # Optional: MAY contain "name", "url", "email"
    'CONTACT': {},
    # Optional: MUST contain "name", MAY contain URL
    'LICENSE': {},
    # Statically set schema version. May also be an empty string. When used together with
    # view versioning, will become '0.0.0 (v2)' for 'v2' versioned requests.
    # Set VERSION to None if only the request version should be rendered.
    'VERSION': '1.0.0',
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    # e.g. [{'url': 'https://example.com/v1', 'description': 'Text'}, ...]
    'SERVERS': [],
    # Tags defined in the global scope
    'TAGS': [],
    # Optional: MUST contain 'url', may contain "description"
    'EXTERNAL_DOCS': {},

    # Arbitrary specification extensions attached to the schema's info object.
    # https://swagger.io/specification/#specification-extensions
    'EXTENSIONS_INFO': {},

    # Arbitrary specification extensions attached to the schema's root object.
    # https://swagger.io/specification/#specification-extensions
    'EXTENSIONS_ROOT': {},

    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://spec.openapis.org/oas/v3.0.3#oauthFlowsObject
    'OAUTH2_FLOWS': [],
    'OAUTH2_AUTHORIZATION_URL': None,
    'OAUTH2_TOKEN_URL': None,
    'OAUTH2_REFRESH_URL': None,
    'OAUTH2_SCOPES': None,
}

# Social Auth Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email, first_name, last_name'
}


# CORS Origin Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'X-CSRFTOKEN',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin',
    'Access-Control-Allow-Origin',
    'Accept-Language',
    'Currency',
    'display'
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


# Email Settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": _("Casty Admin"),

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": _("Casty"),

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": _("Casty"),

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/favicon.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo":  "images/logo.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark":  "images/logo_black.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": _("Welcome To Casty"),

    # Copyright on the footer
    "copyright": _("Casty Development Team"),

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": ["auth.Group", "accounts.User", "profiles.profile"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": _("Home"),  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": _("Charts"), "url": "admin:charts", "permissions": ["auth.view_user"]},
        {"name": _("Send Email"), "url": "admin:send_email", "permissions": ["auth.view_user"]},

        # model admin to link to (Permissions checked against model)
        # {"app": "accounts"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["accounts", ],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.group": "fas fa-users",
        "accounts.user": "fas fa-user",
        "profiles.profile": "fas fa-id-card",
        "profiles.language": "fas fa-globe-americas",
        "profiles.skill": "fas fa-ribbon",
        "agencies.agency": "far fa-building",
        "reports.report": "fas fa-exclamation-triangle",
        "contracts.contract": "fas fa-file-signature",
        "contracts.solocontract": "fas fa-handshake",
        "reviews.Rate": "fas fa-star",
        "info.aboutus": "fas fa-info",
        "info.contactus": "fas fa-headset",
        "info.cookiepolicy": "fas fa-cookie-bite",
        "info.faqs": "fas fa-question",
        "info.headerimage": "fas fa-images",
        "info.privacypolicy": "fas fa-user-secret",
        "info.termsofservice": "fas fa-handshake",
        "info.maininfo": "fas fa-server"
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "css/jazzmin.css",
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"accounts.user": "carousel", "profiles.profile": "carousel",
                                    'agencies.agency': 'carousel'},
    # Add a language dropdown into the admin
    "language_chooser": True,
}


# Translation Settings
IS_MONOLINGUAL = False
LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ar')
TRANSLATABLE_MODEL_MODULES = [
    'info.models',
]
LOCALE_PATHS = [
    BASE_DIR / 'locale'
]


# Money Settings
DEFAULT_CURRENCY = 'EGP'
CURRENCIES = ('EGP', 'USD', 'EUR')
CURRENCY_CHOICES = [
    ('USD', _('USD $')),
    ('EUR', _('EUR €')),
    ('EGP', _('EGP £')),
]
