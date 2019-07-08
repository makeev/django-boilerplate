import logging.config

# DJANGO_LOG_LEVEL = 'DEBUG'
# 'CRITICAL': CRITICAL,
# 'FATAL': FATAL,
# 'ERROR': ERROR,
# 'WARNING': WARNING,
# 'INFO': INFO,
# 'DEBUG': DEBUG,


LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'color_console': {
            '()': 'project.helpers.log_formater.DjangoColorsFormatter',
            'format': '{asctime}.{msecs:03.0f}\t{levelname}\t{name}\t [{filename}:{lineno:d}]\t  {message}',
            'datefmt': '%H:%M:%S',
        },
        # Django runserver request logging format
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(asctime)s.%(msecs)03d %(message)s',
            'datefmt': '%H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'project.helpers.log_formater.StdoutHandler',
            'formatter': 'color_console',
        },

        # Add Handler for Sentry for `xxxx` and above
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },

        # Standard handler for django runserver
        'django.server': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },

        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        # Default runserver request logging
        'django.server': {
            'level': 'INFO',
            'handlers': ['django.server'],
            'propagate': False,
        },
        # Управление логами сетевых соединений,
        # которые заебывают в режиме DEBUG
        'urllib3.connectionpool': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'web3': {
            'level': 'INFO',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sorl.thumbnail.base': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'raven.contrib.django.client.DjangoClient': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        # меньше дублирования в консоль
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        # # отправка писем
        # 'herald.base': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
    },
})
