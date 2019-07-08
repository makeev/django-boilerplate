from collections import OrderedDict

"""
https://django-constance.readthedocs.io/

The supported types:
bool, int, float, Decimal, str, datetime, date, time

Command Line:
./manage.py constance list
./manage.py constance get THE_ANSWER
./manage.py constance set SITE_NAME "Another Title"

Code usage:
from constance import config
config.THE_ANSWER

"""

CONSTANCE_SUPERUSER_ONLY = True

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_CACHE_BACKEND = 'constance'
CONSTANCE_DATABASE_CACHE_AUTOFILL_TIMEOUT = 3600 * 24


CONSTANCE_ADDITIONAL_FIELDS = {
    'input_field': ['django.forms.fields.CharField', {
        'widget': 'django.forms.TextInput',
        'max_length': 100,
        'validators': [],
        'required': False,
    }],
    'url_field': ['django.forms.fields.URLField', {
        'widget': 'django.forms.TextInput',
        'max_length': 100,
        'validators': [],
        'required': False,
    }],
    'email_field': ['django.forms.fields.EmailField', {
        'widget': 'django.forms.TextInput',
        'max_length': 100,
        'validators': [],
        'required': False,
    }],
}

CONSTANCE_CONFIG = OrderedDict([
    ('GOOGLE_MAP_API_KEY', ('', '', 'input_field')),
    ('GOOGLE_TAG_MANAGER_API_KEY', ('', '', 'input_field')),
    ('FACEBOOK_PIXEL_KEY', ('', '', 'input_field')),
    ('MAIN_EMAIL', ('main@site.com', '', 'email_field')),
])


# CONSTANCE_CONFIG_FIELDSETS must contain all fields from CONSTANCE_CONFIG
CONSTANCE_CONFIG_FIELDSETS = OrderedDict([
    ('Other API keys', (
        'GOOGLE_MAP_API_KEY',
        'GOOGLE_TAG_MANAGER_API_KEY',
        'FACEBOOK_PIXEL_KEY',
    )),
    ('Emails', (
        'MAIN_EMAIL',
    )),
])
