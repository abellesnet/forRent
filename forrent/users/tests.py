from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME


class PostApiTestCase(TestCase):
    url_create = reverse('user_create')

    @classmethod
    def setUpClass(cls):
        super(PostApiTestCase, cls).setUpClass()
        call_command('config_project')

    def test_hosts_group_exists(self):
        host_group = Group.objects.filter(name=HOSTS_GROUP_NAME)
        self.assertEqual(len(host_group), 1)

    def test_guests_group_exists(self):
        host_group = Group.objects.filter(name=GUESTS_GROUP_NAME)
        self.assertEqual(len(host_group), 1)
