# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rooms.models import RoomBooking, RoomRating, RoomComment, Room, RoomAmenity
from rooms.permissions import IsBookingOwner, IsAuthorizedGuest, CreateReadOnly
from rooms.serializers import RoomBookingSerializer, RoomRatingSerializer, RoomCommentSerializer, \
    RoomCommentCreateSerializer, RoomSerializer, RoomAmenitySerializer


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


class RoomCommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, CreateReadOnly, ]
    filter_fields = ('room',)

    def get_queryset(self):
        return RoomComment.objects.all().select_related('room', 'author', )

    def get_serializer_class(self):
        if self.action in ('create',):
            return RoomCommentCreateSerializer
        return RoomCommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('host',)


class RoomAmenityViewSet(ReadOnlyModelViewSet):
    queryset = RoomAmenity.objects.all()
    serializer_class = RoomAmenitySerializer
