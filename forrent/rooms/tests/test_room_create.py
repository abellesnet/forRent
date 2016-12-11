# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings

from forrent.settings import HOSTS_GROUP_NAME
from rooms.models import Room


@override_settings(ROOT_URLCONF='rooms.urls')
class MyRoomsListTest(TestCase):
    ROOM_CREATE_URL = '/room/c/'
    USERS_PASSWORD = "the_most_secure_password_in_the_world"

    @classmethod
    def setUpClass(cls):
        super(MyRoomsListTest, cls).setUpClass()
        call_command('config_project')

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password=self.USERS_PASSWORD)
        self.host1 = User.objects.create_user(username='host1', password=self.USERS_PASSWORD)
        self.host1.groups = [(Group.objects.get(name=HOSTS_GROUP_NAME))]
        self.room1 = {
            'name': 'first room',
            'description': 'This is the first room',
            'accommodates': 2,
            'beds': 1,
            'private_bathroom': True,
            'price_per_day': 100,
            'available_since': '2016-10-10',
            'available_to': '2016-12-12',
        }

    def test_if_user_is_not_authenticated_then_redirect(self):
        response = self.client.post(self.ROOM_CREATE_URL, self.room1)
        self.assertEqual(response.status_code, 302)
        created_room = Room.objects.filter(name=self.room1['name']).first()
        self.assertIsNone(created_room)

    def test_if_user_is_not_host_then_redirect(self):
        self.client.login(username='user1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOM_CREATE_URL, self.room1)
        self.assertEqual(response.status_code, 302)
        created_room = Room.objects.filter(name=self.room1['name']).first()
        self.assertIsNone(created_room)

    # def test_the_room_created_has_the_authenticated_host(self):
    #     self.client.login(username='host1', password=self.USERS_PASSWORD)
    #     response = self.client.post(self.ROOM_CREATE_URL, self.room1)
    #     self.assertEqual(response.status_code, 302)
    #     created_room = Room.objects.filter(name=self.room1['name']).first()
    #     self.assertEqual(created_room.host, self.host1)

    # def test_alfter_room_creation_shows_it(self):
    #     self.client.login(username='host1', password=self.USERS_PASSWORD)
    #     response = self.client.post(self.ROOM_CREATE_URL, self.room1, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context['room'].name, self.room1['name'])
