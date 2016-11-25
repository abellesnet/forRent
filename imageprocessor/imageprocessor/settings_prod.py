# -*- coding: utf-8 -*-

from imageprocessor.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*',
]

# Broker

BROKER_HOST = 'broker'

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'errorlogfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_URL, 'error.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'standard',
        },
        'infologfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_URL, 'info.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['errorlogfile'],
            'level': 'ERROR',
        },
        'imageprocessor': {
            'handlers': ['infologfile', ],
            'level': 'INFO',
        },
    }
}


