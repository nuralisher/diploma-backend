from django.urls import path, include
from .views import *


urlpatterns = [
    path('', index, name='main'),
    path('category/<slug:category_slug>/', show_category, name='category'),
    path('product/<slug:product_slug>/', show_product, name='product'),

]
