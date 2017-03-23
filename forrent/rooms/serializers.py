# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.urls import reverse
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from rooms.models import RoomBooking, RoomRating, RoomComment, Room


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


class RoomCommentSerializer(ModelSerializer):
    author_full_name = SerializerMethodField()
    author_url = SerializerMethodField()
    author_photo = SerializerMethodField()

    class Meta:
        model = RoomComment
        fields = ('id', 'room', 'author', 'comment', 'created_at', 'author_full_name', 'author_url', 'author_photo',)

    def get_author_full_name(self, obj):
        return obj.author.get_full_name()

    def get_author_url(self, obj):
        if not hasattr(obj.author, 'profile'):
            return None
        return reverse('profile_detail', kwargs={'pk': obj.author.profile.pk})

    def get_author_photo(self, obj):
        if not hasattr(obj.author, 'profile') or not obj.author.profile.photo:
            return os.path.join(settings.STATIC_URL, "img/no-photo.png")
        return os.path.join(settings.MEDIA_URL, obj.author.profile.photo.name)


class RoomCommentCreateSerializer(ModelSerializer):
    class Meta:
        model = RoomComment
        fields = ('id', 'room', 'comment',)


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        exclude = ('created_at', 'modified_at',)
