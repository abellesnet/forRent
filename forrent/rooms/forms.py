# -*- coding: utf-8 -*-

from django.forms import ModelForm

from rooms.models import Room


class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('host',)


class UpdateRoomForm(CreateRoomForm):
    class Meta(CreateRoomForm.Meta):
        exclude = ('host', 'main_photo',)
