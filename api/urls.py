from django.urls import path
from .views import ListTable, DetailTable

urlpatterns = [
    path('tables/', ListTable.as_view()),
    path('tables/<uuid:pk>/', DetailTable.as_view())
]
