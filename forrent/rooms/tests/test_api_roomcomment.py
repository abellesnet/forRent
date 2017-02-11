from datetime import timedelta

from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings
from django.utils.timezone import now
from rest_framework import status

from forrent.settings import GUESTS_GROUP_NAME
from rooms.models import Room, RoomComment


@override_settings(ROOT_URLCONF='rooms.api_urls')
class RoomCommentGetTest(TestCase):
    ROOMCOMMENT_URL = '/1.0/roomcomment/'
    USERS_PASSWORD = "the_most_secure_password_in_the_world"

    @classmethod
    def setUpClass(cls):
        super(RoomCommentGetTest, cls).setUpClass()
        call_command('config_project')

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password=self.USERS_PASSWORD)
        self.user1.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.room1 = Room.objects.create(
            host=self.user1,
            name='first room',
            description='This is the first room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now(),
            available_to=now() + timedelta(days=10),
        )
        self.comment1 = RoomComment.objects.create(
            room=self.room1,
            author=self.user1,
            comment="First comment"
        )
        self.comment2 = RoomComment.objects.create(
            room=self.room1,
            author=self.user1,
            comment="Second comment"
        )
        self.comment3 = RoomComment.objects.create(
            room=self.room1,
            author=self.user1,
            comment="Last comment"
        )

    def test_search_by_room_works(self):
        response = self.client.get('{0}?room={1}'.format(self.ROOMCOMMENT_URL, self.room1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0].get('room'), self.room1.id)


@override_settings(ROOT_URLCONF='rooms.api_urls')
class RoomCommentPostTest(TestCase):
    ROOMCOMMENT_URL = '/1.0/roomcomment/'
    USERS_PASSWORD = "the_most_secure_password_in_the_world"

    @classmethod
    def setUpClass(cls):
        super(RoomCommentPostTest, cls).setUpClass()
        call_command('config_project')

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password=self.USERS_PASSWORD)
        self.user1.groups = [(Group.objects.get(name=GUESTS_GROUP_NAME))]
        self.room1 = Room.objects.create(
            host=self.user1,
            name='first room',
            description='This is the first room',
            accommodates=2,
            beds=1,
            private_bathroom=True,
            price_per_day=100,
            available_since=now() - timedelta(days=100),
            available_to=now() + timedelta(days=100),
        )
        self.comment1 = {
            'room': self.room1.id,
            'comment': "Comment 1"
        }
        self.comment2 = {
            'room': self.room1.id,
            'comment': "Comment 2"
        }

    def test_if_user_is_not_authenticated_then_forbidden(self):
        response = self.client.post(self.ROOMCOMMENT_URL, data=self.comment1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_comment_works(self):
        self.client.login(username='user1', password=self.USERS_PASSWORD)
        response = self.client.post(self.ROOMCOMMENT_URL, data=self.comment1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
