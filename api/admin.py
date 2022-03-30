from django.contrib import admin
from .models import Table, Menu, Restaurant, MenuCategory

admin.site.register(Table)
admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(MenuCategory)

