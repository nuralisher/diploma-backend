from rest_framework import permissions
from rest_framework import serializers
from api.serializers import RestaurantCreateListSerializer


class IsOwnerAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            request_serializer = RestaurantCreateListSerializer(data=request.data, many=True)
            request_serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return False
        else:
            return request_serializer.data['owner'] == request.user
