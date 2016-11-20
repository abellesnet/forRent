# -*- coding: utf-8 -*-
from django.conf import settings

DEFAULT_IMAGE_SIZE = getattr(settings, 'DEFAULT_IMAGE_SIZE', (1200, 629))
DEFAULT_IMAGE_OPTIONS = getattr(settings, 'DEFAULT_IMAGE_OPTIONS', {'size': DEFAULT_IMAGE_SIZE, 'crop': 'smart'})
