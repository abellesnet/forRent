# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rooms.models import RoomBooking
from rooms.permissions import IsBookingOwner
from rooms.serializers import RoomBookingSerializer


class RoomBookingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsBookingOwner, ]
    serializer_class = RoomBookingSerializer

    def get_queryset(self):
        return RoomBooking.objects.filter(guest=self.request.user).select_related('room', 'guest',)

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
