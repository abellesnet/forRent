# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from rooms.models import Room


class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('host',)
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'accommodates': _('Accommodates'),
            'beds': _('Beds'),
            'private_bathroom': _('Private bathroom'),
            'amenity_set': _('Amenities'),
            'price_per_day': _('Price per day'),
            'available_since': _('Available since'),
            'available_to': _('Available to'),
            'main_photo': _('Main photo'),
        }


class UpdateRoomForm(CreateRoomForm):
    class Meta(CreateRoomForm.Meta):
        exclude = ('host', 'main_photo',)
