
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='ind'),
    path('about/', views.about, name='ab')
]