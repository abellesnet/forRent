# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class IsBookingOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.guest == request.user
