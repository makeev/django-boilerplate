import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)

SITE_ID = 1

SECRET_KEY = '__FAKE__'

INTERNAL_IPS = [
    '0.0.0.0',
    '127.0.0.1',
]

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
]

ADMINS = [
    'admin@localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db/db.sqlite3'),
        'ATOMIC_REQUESTS': True,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 10,
        'OPTIONS': {
            'timeout': 10,
        }
    }
}

REDIS_HOST = 'localhost'
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:6379' % REDIS_HOST,
        'TIMEOUT': 3600 * 3,
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': '',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
        },
    },
    'constance': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:6379' % REDIS_HOST,
        'TIMEOUT': 600,
    },
}

INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'logentry_admin',
    'rest_framework',
    'constance',
    'constance.backends.database',
    'project',
    'main',
    'adminsortable2',
]

DEBUG = True

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'project.middleware.force_default_lang.ForceDefaultLangMiddleware',
]


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # 'project.context_processors.each_context',
            ],
            'loaders': [
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.filesystem.Loader',
            ]
        },
    },
]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # поиск статики в директориях приложений
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(ROOT_DIR, 'www/media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(ROOT_DIR, 'www/static')
STATIC_URL = '/static/'


FIXTURE_DIRS = [BASE_DIR]

WSGI_APPLICATION = 'project.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Argon2 is the winner of the 2015 Password Hashing Competition,
# a community organized open competition to select a next generation hashing algorithm.
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

DATABASE_ROUTERS = [
    # 'project.routers.FiascoRouter',
    # 'project.routers.Cbl4Router',
]

# custom user model
AUTH_USER_MODEL = 'main.User'


EMAIL_CONFIRMATION_SECRET = '__SECRET__'
EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

# CSRF_USE_SESSIONS = False
# CSRF_COOKIE_NAME = 'a_csrf'
# CSRF_COOKIE_PATH = '/admin/'
# CSRF_COOKIE_HTTPONLY ???
# CSRF_COOKIE_SECURE = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'auth.authentication.RequestUserAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'main.drf.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'EXCEPTION_HANDLER': 'main.drf.full_details_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


APPEND_SLASH = False

TIME_ZONE = 'Europe/Moscow'

USE_I18N = False
LANGUAGES = (
    ('en', 'English'),
)
LANGUAGE_CODE = 'en'

LOCALE_PATHS = (os.path.join(ROOT_DIR, 'locale'),)

USE_L10N = False
USE_TZ = True


DATE_FORMAT = 'd.m.Y'
SHORT_DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y, H:i:s'
SHORT_DATETIME_FORMAT = 'd.m.Y, H:i'

TIME_FORMAT = 'H:i:s'
SHORT_TIME_FORMAT = 'H:i'


DEFAULT_FILE_STORAGE = 'project.helpers.services.ASCIIFileSystemStorage'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Default Noreply <noreply@site.com>'
