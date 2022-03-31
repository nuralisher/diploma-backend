from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
import time

def index(request):
    category = MainCategories.objects.all()
    product = Products.objects.all()
    context = {
        'category': category,
        'product': product,
        'cat_selected': 0,
    }
    return render(request, 'menu/index.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_category(request, category_slug):
    category = get_object_or_404(MainCategories, slug=category_slug)
    productByCat = Products.objects.filter(cat_id=category.pk)
    context = {
        'category': category,
        'product': productByCat,
        # 'cat_selected': productByCat.cat_id,
    }
    return render(request, 'menu/category.html', context=context)


def show_product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    context = {
        'product': product,
        'cat_selected': product.cat_id,
    }
    return render(request, 'menu/product.html', context=context)

def basket():
    name = 'zero'
    return name












# def qrID(request, numberPlace):
#     return HttpResponse(f"<h2>number by QR is {numberPlace}</h2>")

# def index(request, numberPlace):
    # mainCategories = MainCategories.objects.order_by('-id')[:100]
    # # return HttpResponse(f"<h2>number by QR is {numberPlace}</h2>")
    # num = numberPlace
    # if numberPlace>99:
    #     # raise Http404()   
    #     time.sleep(0)
    #     return redirect('/99/menu', permanent=False)
    # if (request.GET):
    #     print(request.GET)
    # return render(request, 'menu/index.html', { 
    #     'qrID' : num,
    #     'title': 'main page', 'mainCategories': mainCategories })

# def about(request):
#     return render(request, 'menu/about.html')

# def unFound(request, exception):
#     return HttpResponseNotFound('<h1>page is absent</h1>')