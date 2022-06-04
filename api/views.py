import logging

import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics, status

from user_management.models import Employee, Client
from user_management.serializers import EmployeeRegistrationSerializer, RestaurantsEmployeesSerializer
from .models import Table, Menu, Restaurant, MenuCategory, Position, Order, OrderItem, PositionManager
from .serializers import TableSerializer, MenuSerializer, RestaurantSerializer, TableDetailSerializer, \
    MenuCategorySerializer, RestaurantCreateListSerializer, PositionSerializer, OrderSerializer, OrderDetailSerializer, \
    UserSerializer, ProfileEmployeeSerializer, ProfileClientSerializer
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.filters import *


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


class EmployeeList(GenericAPIView):
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'user__email']

    def get(self, request):
        employees = self.filter_queryset(Employee.objects.all())
        serializer = RestaurantsEmployeesSerializer(employees, many=True)
        employeesList = []
        for employee in serializer.data:
            user = User.objects.get(id=employee['user_id'])
            data = {
                'id': employee['id'],
                'full_name': employee['first_name'] + ' ' + employee['last_name'],
                'email': user.email,
            }
            employeesList.append(data)
        return JsonResponse(employeesList, safe=False)


@api_view(['GET', 'POST'])
def list_add_restaurant_employee(request, pk):
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)
    if request.method == 'GET':
        try:
            employees = Employee.objects.filter(restaurants__in=[restaurant])
        except Employee.DoesNotExist as e:
            return JsonResponse([], safe=False)
        serializer = RestaurantsEmployeesSerializer(employees, many=True)
        employeesList = []
        for employee in serializer.data:
            user = User.objects.get(id=employee['user_id'])
            position = Position.objects.get(employee_id=employee['id'], restaurant_id=restaurant.id)
            data = {
                'id': employee['id'],
                'full_name': employee['first_name'] + ' ' + employee['last_name'],
                'email': user.email,
                'position': position.type,
            }
            employeesList.append(data)
        return JsonResponse(employeesList, safe=False)
    if request.method == 'POST':
        try:
            request.data['employeeID']
        except KeyError:
            return JsonResponse({'error': 'employee ID required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            request.data['position']
        except KeyError:
            return JsonResponse({'error': 'position required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = Employee.objects.get(id=request.data['employeeID'])
        except Employee.DoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False)

        try:
            position = Position.PositionType[request.data['position']]
        except:
            return JsonResponse({'error': 'no such position type'}, status=status.HTTP_400_BAD_REQUEST)
        Position.objects.create_position(employee, restaurant, position)
        restaurant.employees.add(employee)
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
        try:
            client = Client.objects.get(user_id=self.request.user.id)
        except Client.DoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        order = serializer.save(client=client)
        order_items = self.request.data['order_items']
        for order_item in order_items:
            OrderItem.objects.create_order_item(order_item['menu'], order, order_item['quantity'])


class OrderDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer


@api_view(['GET'])
def restaurant_orders(request, pk):
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)
    if request.method == 'GET':
        try:
            order = Order.objects.filter(restaurant=restaurant)
        except Order.DoesNotExist as e:
            return JsonResponse([], safe=False)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def me(request):
    try:
        client = Client.objects.get(user_id=request.user.id)
        serializer = ProfileClientSerializer(client)
        return Response(serializer.data)
    except:
        try:
            employee = Employee.objects.get(user_id=request.user.id)
            serializer = ProfileEmployeeSerializer(employee)
            return Response(serializer.data)
        except:
            return JsonResponse({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


