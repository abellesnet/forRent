# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group, User, Permission
from django.core.management import BaseCommand

from forrent.settings import HOSTS_GROUP_NAME, GUESTS_GROUP_NAME


def set_hosts_group_premissions(hosts_group):
    permission = Permission.objects.get(codename='add_room')
    hosts_group.permissions.add(permission)
    permission = Permission.objects.get(codename='change_room')
    hosts_group.permissions.add(permission)
    permission = Permission.objects.get(codename='delete_room')
    hosts_group.permissions.add(permission)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = User.objects.get_or_create(username='admin')
        if created:
            admin_user.set_password('admin')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()

        # Create groups
        hosts_group, created = Group.objects.get_or_create(name=HOSTS_GROUP_NAME)
        if created:
            set_hosts_group_premissions(hosts_group)
        guests_group, created = Group.objects.get_or_create(name=GUESTS_GROUP_NAME)
