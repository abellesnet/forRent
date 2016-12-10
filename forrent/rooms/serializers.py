# -*- coding: utf-8 -*-
from rest_framework.fields import SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

from rooms.models import RoomBooking


class RoomBookingSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = RoomBooking
        fields = ('room', 'since', 'to', 'total_price', 'url',)

    def get_url(self, obj):
        return reverse(viewname='roombooking-detail', kwargs={'pk': obj.pk}).format(obj)
