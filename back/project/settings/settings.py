import os
from django.urls import reverse_lazy

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

CACHE_BACKEND = 'django.core.cache.backends.memcached.MemcachedCache'
MEMCACHED_LOCATION = '127.0.0.1:11211'
CACHES = {
    'default': {
        'BACKEND': CACHE_BACKEND,
        'LOCATION': MEMCACHED_LOCATION,
        'TIMEOUT': 3600 * 3,
    },
    'constance': {
        'BACKEND': CACHE_BACKEND,
        'LOCATION': MEMCACHED_LOCATION,
        'TIMEOUT': 600,
    },
}

RQ = {
    'DEFAULT_RESULT_TTL': 50,
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'email': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}

RAVEN_CONFIG = {
    'dsn': None,
}

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'modeltranslation',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'logentry_admin',
    'sorl.thumbnail',
    'rest_framework',
    'django_rq',
    'constance',
    'constance.backends.database',
    'rangefilter',
    'admin_comments',
    'django_cron',
    'project',
    'main',
    'adminsortable2',  # fixme: должно быть после project до фикса django-admin-sortable2 issue #202 #206
    'boolean_switch',
    'news',
]

# отступ в пикселях для дочерних элементов в админке
MPTT_ADMIN_LEVEL_INDENT = 20

# кроны
CRON_CLASSES = [
    # 'main.cron.CronTest',
]
DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 30
FAILED_RUNS_CRONJOB_EMAIL_PREFIX = "[Server check]: "


LOGIN_URL = reverse_lazy('main:home')
LOGOUT_REDIRECT_URL = reverse_lazy('main:home')


DEBUG = True
THUMBNAIL_DEBUG = False
THUMBNAIL_ENGINE = 'main.sorl.FixedEngine'  # исправление бага с превью для PNG mode=P

THUMBNAIL_QUALITY = 85
THUMBNAIL_PROGRESSIVE = False  # он всё равно не работает

# REDIS
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_DB = 1
THUMBNAIL_REDIS_PASSWORD = ''
THUMBNAIL_REDIS_HOST = '127.0.0.1'
THUMBNAIL_REDIS_PORT = 6379


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
    # 'pipeline.middleware.MinifyHTMLMiddleware',
    'project.middleware.force_default_lang.ForceDefaultLangMiddleware',  # использовать язык по умолчанию, а не HTTP_ACCEPT_LANGUAGE
    # 'admin_reorder.middleware.ModelAdminReorder',
]


# настройки против ip-спуфинга
# XFF_STRICT = True  # Strict mode will stop all failing requests
# XFF_ALWAYS_PROXY = True  # обрабатывать только запросы, прошедшие через Nginx
# XFF_TRUSTED_PROXY_DEPTH = 1  # ровно один Nginx


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    # Стардартные шаблоны Django для админки и чужих приложений
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'project/templates')],
        'APP_DIRS': False,
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

# своя модель для пользователей
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
        'main.drf.CustomJSONRenderer',  # чтобы сериалайзить Money и всякое такое
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'EXCEPTION_HANDLER': 'main.drf.full_details_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


APPEND_SLASH = False

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)
LANGUAGE_CODE = 'en'
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE
MODELTRANSLATION_AUTO_POPULATE = False

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
