# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rooms.models import RoomBooking, RoomRating
from rooms.permissions import IsBookingOwner, IsAuthorizedGuest
from rooms.serializers import RoomBookingSerializer, RoomRatingSerializer


class RoomBookingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsBookingOwner, ]
    serializer_class = RoomBookingSerializer

    def get_queryset(self):
        return RoomBooking.objects.filter(guest=self.request.user).select_related('room', 'guest', )

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)


class RoomRatingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorizedGuest, ]
    serializer_class = RoomRatingSerializer
    filter_fields = ('room',)

    def get_queryset(self):
        return RoomRating.objects.filter(guest=self.request.user).select_related('room', 'guest', )

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
