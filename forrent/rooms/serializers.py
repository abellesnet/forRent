# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from rooms.models import RoomBooking, RoomRating


class RoomBookingSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = RoomBooking
        fields = ('room', 'since', 'to', 'total_price', 'url',)

    def get_url(self, obj):
        return reverse('roombooking_list')


class RoomRatingSerializer(ModelSerializer):
    class Meta:
        model = RoomRating
        fields = ('id', 'room', 'rate',)
