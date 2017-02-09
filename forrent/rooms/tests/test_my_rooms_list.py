from datetime import timedelta

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings
from django.utils.timezone import now

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME
from rooms.models import Room


@override_settings(ROOT_URLCONF='rooms.urls')
class MyRoomsListTest(TestCase):
    MY_ROOMS_URL = '/myrooms/'
    USERS_PASSWORD = "the_most_secure_password_in_the_world"

    @classmethod
    def setUpClass(cls):
        super(MyRoomsListTest, cls).setUpClass()
        call_command('config_project')

    def setUp(self):
        self.guest1 = User.objects.create_user(username='guest1', password=self.USERS_PASSWORD)
        self.guest1.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.host1 = User.objects.create_user(username='host1', password=self.USERS_PASSWORD)
        self.host1.groups = [(Group.objects.get(name=HOSTS_GROUP_NAME))]
        self.host2 = User.objects.create_user(username='host2', password=self.USERS_PASSWORD)
        self.host2.groups = [(Group.objects.get(name=HOSTS_GROUP_NAME))]
        self.host3 = User.objects.create_user(username='host3', password=self.USERS_PASSWORD)
        self.host3.groups = [(Group.objects.get(name=HOSTS_GROUP_NAME))]
        self.room1 = Room.objects.create(
            host=self.host1,
            name='first room',
            description='This is the first room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now(),
            available_to=now() + timedelta(days=10),
        )
        self.room1 = Room.objects.create(
            host=self.host2,
            name='second room',
            description='This is the second room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now(),
            available_to=now() + timedelta(days=10),
        )
        self.room1 = Room.objects.create(
            host=self.host1,
            name='third room',
            description='This is the third room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now(),
            available_to=now() + timedelta(days=10),
        )

    def test_if_user_is_not_authenticated_then_redirect(self):
        response = self.client.get(self.MY_ROOMS_URL)
        self.assertEqual(response.status_code, 302)

    def test_if_user_is_not_host_then_return_empty_list(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.get(self.MY_ROOMS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['room_list']), 0)

    def test_every_listed_room_belongs_authenticated_user(self):
        self.client.login(username='host1', password=self.USERS_PASSWORD)
        response = self.client.get(self.MY_ROOMS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['room_list']), 2)
        for room in response.context['room_list']:
            self.assertEqual(room.host, self.host1)

    def test_every_authenticated_user_rooms_are_listed(self):
        self.client.login(username='host2', password=self.USERS_PASSWORD)
        response = self.client.get(self.MY_ROOMS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['room_list']), 1)

    def test_if_host_has_no_rooms_return_empty_list(self):
        self.client.login(username='host3', password=self.USERS_PASSWORD)
        response = self.client.get(self.MY_ROOMS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['room_list']), 0)
