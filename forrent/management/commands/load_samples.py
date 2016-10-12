# -*- coding: utf-8 -*-
from random import randint

from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand, call_command

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME
from rooms.models import RoomAmenity


def create_users(user_names=()):
    available_groups = [
        Group.objects.get(name=HOSTS_GROUP_NAME),
        Group.objects.get(name=GUESTS_GROUP_NAME)
    ]
    for user in user_names:
        first_name = user.split(' ')[0]
        last_name = user[len(first_name) + 1:]
        username = first_name.lower()
        email = username + '@bigbangtheory.com'
        user_created, created = User.objects.get_or_create(username=username, email=email,
                                                           first_name=first_name, last_name=last_name, )
        if created:
            user_created.set_password(username)
            user_created.groups = [available_groups[randint(0, 1)], ]
            user_created.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('config_project')
        create_users((
            'Sheldon Cooper',
            'Penny Penny Penny',
            'Leonard Hofstadter',
            'Howard Wolowitz',
            'Raj Koothrappali',
            'Amy Farrah Fowler',
        ))

        room_amenities = ('Internet', 'Kitchen', 'TV', 'Heating', 'Air conditioning', 'Washer', 'Pets allowed',)
        for amenity in room_amenities:
            RoomAmenity.objects.get_or_create(name=amenity)
