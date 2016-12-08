# -*- coding: utf-8 -*-
import tempfile
from datetime import timedelta
from random import randint, uniform

import requests
from django.contrib.auth.models import User, Group
from django.core import files
from django.core.management import BaseCommand, call_command
from django.utils import timezone

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME
from rooms.models import RoomAmenity, Room
from users.models import Profile

ROOM_SET_SIZE = 50
ROOM_MEDIA_URL = 'http://lorempixel.com/1200/629/city'


def download_image_file(image_url):
    request = requests.get(image_url, stream=True)
    temporary_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    for block in request.iter_content(1024 * 8):
        if not block:
            break
        temporary_file.write(block)
    return format(temporary_file.name.split('/')[-1]), temporary_file


def create_users(users=()):
    for user in users:
        user_full_name = user[0]
        first_name = user_full_name.split(' ')[0]
        last_name = user_full_name[len(first_name) + 1:]
        username = first_name.lower()
        email = username + '@bigbangtheory.com'
        user_created, created = User.objects.get_or_create(username=username, email=email,
                                                           first_name=first_name, last_name=last_name, )
        if created:
            user_created.set_password(username)
            user_created.groups = [Group.objects.get(name=user[1]), ]
            user_created.save()
            profile, created = Profile.objects.get_or_create(user=user_created)
            file_name, file = download_image_file(user[2])
            profile.photo.save(file_name, files.File(file))
            profile.save()


def create_room_amenities(room_amenities=()):
    for amenity in room_amenities:
        RoomAmenity.objects.get_or_create(name=amenity)


def create_rooms(size=0):
    hosts = User.objects.filter(is_superuser=False, groups__name=HOSTS_GROUP_NAME)
    room_amenities = RoomAmenity.objects.all()
    for room_number in range(size):
        print('Creating room {0} of {1}'.format(room_number + 1, size))
        description = requests.get('http://loripsum.net/api/plaintext').text
        words = description.split(' ')
        long = randint(3, 5)
        name = ' '.join(words[randint(0, len(words) - long):][:long]) \
            .replace(',', '').replace(';', '').replace(':', '').replace('-', '').replace('.', '').replace('\n', ' ') \
            .capitalize()
        amenities_set = []
        for i in range(randint(0, len(room_amenities))):
            if room_amenities[i] not in amenities_set:
                amenities_set.append(room_amenities[i])
        random_date = timezone.now() + timedelta(days=randint(-30, 90))
        room_created = Room(
            host=hosts[randint(0, len(hosts) - 1)],
            name=name,
            description=description,
            accommodates=randint(1, 4),
            beds=randint(1, 2),
            private_bathroom=randint(0, 1),
            price_per_day=round(uniform(10, 50), 2),
            available_since=random_date,
            available_to=random_date + timedelta(days=randint(7, 120))
        )
        file_name, file = download_image_file(ROOM_MEDIA_URL)
        room_created.main_photo.save(file_name, files.File(file))
        room_created.amenities = amenities_set
        room_created.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('config_project')

        create_users((
            ('Sheldon Cooper', GUESTS_GROUP_NAME,
             'http://javiercantera.com/wp-content/uploads/2015/02/tumblr_static_dc056b4f8c9493f3c64e6e0a85382b31.jpg'),
            ('Penny Penny Penny', HOSTS_GROUP_NAME,
             'http://www.tentacionesdemujer.com/wordpress/wp-content/uploads/2015/01/FACE.jpg'),
            ('Leonard Hofstadter', GUESTS_GROUP_NAME,
             'https://pbs.twimg.com/profile_images/2654852680/87ee5ed912ea7364a29a380be9b22285.jpeg'),
            ('Howard Wolowitz', GUESTS_GROUP_NAME,
             'http://vignette2.wikia.nocookie.net/bigbangtheory/images/6/6a/Howardwolowitz.jpg'),
            ('Raj Koothrappali', GUESTS_GROUP_NAME,
             'http://vaais.com/Files/images/personajes/216.jpg'),
            ('Amy Farrah Fowler', HOSTS_GROUP_NAME,
             'http://gorabbit.ru/upload/iblock/fd0/fd059a0ec3f3cd284592312e1b1706af.jpg'),
        ))

        create_room_amenities(
            ('Internet', 'Kitchen', 'TV', 'Heating', 'Air conditioning', 'Washer', 'Pets allowed',)
        )

        create_rooms(ROOM_SET_SIZE)
