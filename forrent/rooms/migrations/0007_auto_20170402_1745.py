# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-02 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_roomcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='map',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]