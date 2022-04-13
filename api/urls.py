from django.urls import path
from .views import ListTable, DetailTable, MenuList, MenuDetail, RestaurantList, RestaurantDetail, MenuCategoryList, \
    MenuCategoryDetail, restaurantCategories, categoryMenus, PositionList, PositionDetail, get_my_restaurants

urlpatterns = [
    path('tables/', ListTable.as_view()),
    path('tables/<uuid:pk>/', DetailTable.as_view()),
    path('menus/', MenuList.as_view()),
    path('menus/<int:pk>/', MenuDetail.as_view()),
    path('menu-categories/', MenuCategoryList.as_view()),
    path('menu-categories/<int:pk>/', MenuCategoryDetail.as_view()),
    path('restaurants/', RestaurantList.as_view()),
    path('my-restaurants', get_my_restaurants),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view()),
    path('restaurants/<int:pk>/menu-categories/', restaurantCategories),
    path('menu-categories/<int:pk>/menus/', categoryMenus),
    path('positions/', PositionList.as_view()),
    path('positions/<int:pk>', PositionDetail.as_view()),
]
