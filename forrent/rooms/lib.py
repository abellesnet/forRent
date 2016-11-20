# -*- coding: utf-8 -*-
from celery import shared_task
from easy_thumbnails.files import generate_all_aliases

from rooms.models import Room


@shared_task
def generate_responsive_room_main_photo_images(room_pk):
    room = Room.objects.get(pk=room_pk)
    generate_all_aliases(room.main_photo, True)
