from django.urls import path
from .views import *

urlpatterns = [
    # Tables
    path('tables/', ListTable.as_view()),
    path('tables/<uuid:pk>/', DetailTable.as_view()),
    path('restaurants/<int:pk>/tables/', restaurant_tables),

    # Menus
    path('menus/', MenuList.as_view()),
    path('menus/<int:pk>/', MenuDetail.as_view()),
    path('restaurants/<int:pk>/menus/', get_restaurant_menus),
    path('menu-categories/<int:pk>/menus/', categoryMenus),

    # Categories
    path('menu-categories/', MenuCategoryList.as_view()),
    path('menu-categories/<int:pk>/', MenuCategoryDetail.as_view()),
    path('restaurants/<int:pk>/menu-categories/', restaurantCategories),

    # Restaurants
    path('restaurants/', RestaurantList.as_view()),
    path('my-restaurants/', get_my_restaurants),
    path('all-restaurants/', get_all_restaurants),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view()),


    path('restaurants/<int:pk>/employees/', list_add_restaurant_employee),
    path('restaurants/employees/', update_or_delete_employee),

    # Orders
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>/', OrderDetail.as_view()),
    path('restaurants/<int:pk>/orders/', restaurant_orders),

    # Calls
    path('calls/', CallList.as_view()),
    path('calls/<int:pk>/', CallDetail.as_view()),
    path('calls/<int:pk>/close/', close_call),
    path('calls/<int:pk>/cancel/', cancel_call),
    path('restaurants/<int:pk>/calls/', restaurant_calls),
    path('my-call/', get_status_call),
    path('tables/<uuid:pk>/call/', table_call),

    # Positions
    path('positions/', PositionList.as_view()),
    path('positions/<int:pk>', PositionDetail.as_view()),


    # me
    path('me/', me),

    # employee
    path('employees/', EmployeeList.as_view())
]

