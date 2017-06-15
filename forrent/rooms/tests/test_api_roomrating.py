from datetime import timedelta

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase
from django.test import override_settings
from django.utils.timezone import now
from rest_framework import status

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME
from rooms.models import Room, RoomRating, RoomBooking


@override_settings(ROOT_URLCONF='rooms.api_urls')
class RoomRatingGetTest(TestCase):
    ROOMRATING_URL = '/1.0/roomrating/'
    USERS_PASSWORD = "the_most_secure_password_in_the_world"

    @classmethod
    def setUpClass(cls):
        super(RoomRatingGetTest, cls).setUpClass()
        call_command('config_project')

    def setUp(self):
        self.guest1 = User.objects.create_user(username='guest1', password=self.USERS_PASSWORD)
        self.guest1.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.guest2 = User.objects.create_user(username='guest2', password=self.USERS_PASSWORD)
        self.guest2.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.host1 = User.objects.create_user(username='host1', password=self.USERS_PASSWORD)
        self.host1.groups = [(Group.objects.get(name=HOSTS_GROUP_NAME))]
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
        self.room2 = Room.objects.create(
            host=self.host1,
            name='second room',
            description='This is the second room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now(),
            available_to=now() + timedelta(days=10),
        )
        self.rating1 = RoomRating.objects.create(
            room=self.room1,
            guest=self.guest1,
            rate=1
        )
        self.rating2 = RoomRating.objects.create(
            room=self.room1,
            guest=self.guest2,
            rate=2
        )
        self.rating3 = RoomRating.objects.create(
            room=self.room2,
            guest=self.guest1,
            rate=3
        )

    def test_if_user_is_not_authenticated_then_forbidden(self):
        response = self.client.get(self.ROOMRATING_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_only_user_owner_ratings(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.get(self.ROOMRATING_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_by_room_works(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.get('{0}?room={1}'.format(self.ROOMRATING_URL, self.room1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('room'), self.room1.id)


@override_settings(ROOT_URLCONF='rooms.api_urls')
class RoomRatingPostTest(TestCase):
    ROOMRATING_URL = '/1.0/roomrating/'
    USERS_PASSWORD = "the_most_secure_password_in_the_world"

    @classmethod
    def setUpClass(cls):
        super(RoomRatingPostTest, cls).setUpClass()
        call_command('config_project')

    def setUp(self):
        self.guest1 = User.objects.create_user(username='guest1', password=self.USERS_PASSWORD)
        self.guest1.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.guest2 = User.objects.create_user(username='guest2', password=self.USERS_PASSWORD)
        self.guest2.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.host1 = User.objects.create_user(username='host1', password=self.USERS_PASSWORD)
        self.host1.groups = [(Group.objects.get(name=HOSTS_GROUP_NAME))]
        self.room1 = Room.objects.create(
            host=self.host1,
            name='first room',
            description='This is the first room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now() - timedelta(days=100),
            available_to=now() + timedelta(days=100),
        )
        self.room2 = Room.objects.create(
            host=self.host1,
            name='second room',
            description='This is the second room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now() - timedelta(days=100),
            available_to=now() + timedelta(days=100),
        )
        self.booking1 = RoomBooking.objects.create(
            room=self.room1,
            guest=self.guest1,
            since=now() - timedelta(days=50),
            to=now() - timedelta(days=40),
            total_price=100
        )
        self.rating1 = {
            'room': self.room1.id,
            'rate': 1
        }
        self.rating2 = {
            'room': self.room2.id,
            'rate': 1
        }

    def test_if_user_is_not_authenticated_then_forbidden(self):
        response = self.client.post(self.ROOMRATING_URL, data=self.rating1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_no_room_then_forbidden(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOMRATING_URL, data={'rate': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_no_past_booking_then_forbidden(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOMRATING_URL, data=self.rating2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_rating_works(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOMRATING_URL, data=self.rating1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_two_ratings_raises_error(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOMRATING_URL, data=self.rating1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(IntegrityError):
            self.client.post(self.ROOMRATING_URL, data=self.rating1)

    def test_update_ratings_works(self):
        self.client.login(username='guest1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOMRATING_URL, data=self.rating1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_rating_id = response.data.get('id')
        self.rating1['rate'] = 3
        response = self.client.put('{0}{1}'.format(self.ROOMRATING_URL, new_rating_id), data=self.rating1, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
