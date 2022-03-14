from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import MainCategories

def index(request):
    mainCategories = MainCategories.objects.order_by('-id')[:100]
    return render(request, 'menu/index.html', { 'title': 'main page', 'mainCategories': mainCategories })

def about(request):
    return render(request, 'menu/about.html')