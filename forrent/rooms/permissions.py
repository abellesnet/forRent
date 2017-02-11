# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

from rooms.models import Room


class IsBookingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.guest == request.user


class IsAuthorizedGuest(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create',):
            if request.data.get('room'):
                room = Room.objects.get(pk=request.data.get('room'))
                if request.user in room.get_past_guests():
                    return True
        if view.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.guest == request.user


class CreateReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('list', 'retrieve', 'create',):
            return True
        return False
