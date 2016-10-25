# -*- coding: utf-8 -*-
from easy_thumbnails.files import generate_all_aliases


def generate_responsive_images(image):
    generate_all_aliases(image, True)
