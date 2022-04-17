from rest_framework import serializers
from .models import Table, Restaurant, Menu, MenuCategory, Position


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('id', 'qr_code', 'restaurant')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'category', 'price', 'description', 'image')


class MenuCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuCategory
        fields = ('id', 'name', 'restaurant', 'menus')


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_categories', 'tables')


class RestaurantCategory(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ('id', 'name')

class TableRestaurantSerializer(serializers.ModelSerializer):
    menu_categories = RestaurantCategory(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_categories')


class TableDetailSerializer(serializers.ModelSerializer):
    restaurant = TableRestaurantSerializer()

    class Meta:
        model = Table
        fields = ('id', 'qr_code', 'restaurant')



class RestaurantCreateListSerializer(serializers.ModelSerializer):
    menu_categories = MenuCategorySerializer(read_only=True, many=True)
    tables = TableRestaurantSerializer(read_only=True, many=True)
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_categories', 'tables', 'owner')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'type', 'employee', 'restaurant')


