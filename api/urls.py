from django.urls import path
from .views import ListTable, DetailTable, MenuList, MenuDetail, RestaurantList, RestaurantDetail

urlpatterns = [
    path('tables/', ListTable.as_view()),
    path('tables/<uuid:pk>/', DetailTable.as_view()),
    path('menus/', MenuList.as_view()),
    path('menus/<int:pk>/', MenuDetail.as_view()),
    path('restaurants/', RestaurantList.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view()),
]
