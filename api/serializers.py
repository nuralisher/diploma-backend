from rest_framework import serializers
from .models import Table, Restaurant, Menu, MenuCategory, Position, OrderItem, Order


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('id', 'qr_code', 'restaurant', 'number')


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
    # menu_categories = RestaurantCategory(many=True)

    class Meta:
        model = Restaurant
        fields = ('id',)


class TableDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('id', 'qr_code', 'restaurant', 'number')



class RestaurantCreateListSerializer(serializers.ModelSerializer):
    menu_categories = MenuCategorySerializer(read_only=True, many=True)
    tables = TableSerializer(read_only=True, many=True)
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_categories', 'tables', 'owner')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'type', 'employee', 'restaurant')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'menu', 'quantity')


class OrderItemWithoutIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menu', 'quantity')


class TableNumberField(serializers.RelatedField):
    def to_representation(self, value):
        return value.number

class OrderSerializer(serializers.ModelSerializer):
    # order_items = serializers.RelatedField(many=True)
    client = serializers.CharField(read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)
    table = TableNumberField(read_only=True)
    table_id = serializers.UUIDField()

    class Meta:
        model = Order
        fields = ('id', 'table_id',  'table', 'restaurant', 'client', 'created', 'comment', 'order_items')



class MenuPriceField(serializers.RelatedField):
    def to_representation(self, value):
        return value.price


class OrderItemDetailSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='menu', read_only=True)
    price = MenuPriceField(source='menu', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'price', 'quantity')


class TotalCostField(serializers.RelatedField):
    def to_representation(self, value):
        total = 0
        for item in value:
            total += item.price
        return total


class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'table_id',  'table', 'client', 'created', 'comment', 'order_items',)

