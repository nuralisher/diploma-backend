from django.contrib import admin
from .models import *

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture', 'title', 'cat')
    # list_display_links('id','name')
    search_fields = ('name', 'title')
    list_editable = ('name', 'picture', 'title')
    prepopulated_fields = {'slug': ('name',)}

class MainCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    # list_editable = ('name', 'picture')
    # list_filter = ()
    prepopulated_fields = {"slug": ('name',)}


admin.site.register(MainCategories, MainCategoriesAdmin)
admin.site.register(Products, ProductsAdmin)