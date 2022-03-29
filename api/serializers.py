from rest_framework import serializers
from .models import Table, Restaurant, Menu

class TableSerializer(serializers.ModelSerializer):
    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Table
        fields = ('id', 'qr_code', 'restaurant')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'restaurant')


class RestaurantSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menus', 'tables')


class TableDetailSerializer(serializers.ModelSerializer):
    qr_code = serializers.ImageField(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Table
        fields = ('id', 'qr_code', 'restaurant')
