import logging

import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics, status

from user_management.models import Employee
from user_management.serializers import EmployeeRegistrationSerializer
from .models import Table, Menu, Restaurant, MenuCategory, Position, Order, OrderItem
from .serializers import TableSerializer, MenuSerializer, RestaurantSerializer, TableDetailSerializer, \
    MenuCategorySerializer, RestaurantCreateListSerializer, PositionSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

class ListTable(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class DetailTable(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableDetailSerializer

class MenuList(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuCategoryList(generics.ListCreateAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class MenuCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class RestaurantList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantCreateListSerializer

    def perform_create(self, serializer):
        try:
            employee = Employee.objects.get(user_id=self.request.user.id)
        except Employee.DoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False)
        serializer.save(owner=employee)


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

@api_view(['GET', 'POST'])
def restaurantCategories(request, pk):
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    if request.method == 'GET':
        categories = MenuCategory.objects.filter(restaurant_id=pk)
        serializer = MenuCategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MenuCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
def categoryMenus(request, pk):
    try:
        restaurant = MenuCategory.objects.get(id=pk)
    except MenuCategory.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    if request.method == 'GET':
        menus = Menu.objects.filter(category_id=pk)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = Menu(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PositionList(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


@api_view(['GET'])
def get_my_restaurants(request):
    try:
        employee = Employee.objects.get(user_id=request.user.id)
    except Employee.DoesNotExist as e:
        return JsonResponse([], safe=False)
    if request.method == 'GET':
        restaurants = Restaurant.objects.filter(owner_id=employee.id) | Restaurant.objects.filter(employees__in=[employee])
        serializer = RestaurantCreateListSerializer(restaurants, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_all_restaurants(request):
    try:
        employee = Employee.objects.get(user_id=request.user.id)
    except Employee.DoesNotExist as e:
        serializer = RestaurantCreateListSerializer(Restaurant.objects.all(), many=True)
        return Response(serializer.data)
    if request.method == 'GET':
        restaurants = Restaurant.objects.exclude(owner_id=employee.id) | Restaurant.objects.filter(employees__in=[employee])
        serializer = RestaurantCreateListSerializer(restaurants, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def list_add_restaurant_employee(request, pk):
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)
    if request.method == 'GET':
        try:
            employees = Employee.objects.get(restaurants__in=[restaurant])
        except Employee.DoesNotExist as e:
            return JsonResponse([], safe=False)
        serializer = EmployeeRegistrationSerializer(employees, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        try:
            employee = Employee.objects.get(id=request.data.employeeId)
        except Employee.DoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False)
        restaurant.employees.push(employee)
        restaurant.save()
        serializer = RestaurantCreateListSerializer(restaurant)
        return Response(serializer.data)


# @api_view(['GET', 'POST', 'DELETE'])
# def select_restaurant(request, pk):
#     try:
#         employee = Employee.objects.get(user_id=request.user.id)
#     except Employee.DoesNotExist as e:
#         return JsonResponse({'error': str(e)}, safe=False)
#
#     if request.method == 'GET':
#


@api_view(['GET'])
def restaurant_tables(request, pk):
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    serializer = TableSerializer(restaurant.tables, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_image(request):
    if (request.method == 'GET'):
        return HttpResponse(requests.get(request.query_params.get('url')), content_type='image/svg+xml')


@api_view(['GET'])
def get_restaurant_menus(request, pk):
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)
    categories = MenuCategory.objects.filter(restaurant_id=restaurant.id)
    menus = Menu.objects.filter(category__in=categories)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)



class OrderList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        order_items = self.request.data['order_items']
        for order_item in order_items:
            OrderItem.objects.create_order_item(order_item['menu'], order, order_item['quantity'])


@api_view(['GET', 'POST'])
def create_order(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        order_data = {'client': data['client'], 'restaurant': data['restaurant']}
        order_items = data['order_items']
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer._errors, status=status.HTTP_400_BAD_REQUEST)

# PROBOO

class OrderDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


