# -*- coding: utf-8 -*-
from django.conf import settings

DEFAULT_PROFILE_PHOTO_SIZE = getattr(settings, 'DEFAULT_PROFILE_PHOTO_SIZE', (128, 128))
DEFAULT_PROFILE_PHOTO_OPTIONS = getattr(
    settings, 'DEFAULT_PROFILE_PHOTO_OPTIONS', {'size': DEFAULT_PROFILE_PHOTO_SIZE, 'crop': 'smart'}
)
