from django.shortcuts import render
from rest_framework import generics
from .models import Table
from .serializers import TableSerializer

class ListTable(generics.ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class DetailTable(generics.RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
