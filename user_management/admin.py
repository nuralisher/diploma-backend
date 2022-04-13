from django.contrib import admin

from user_management.models import User, Client, Employee

# admin.site.register(User)
admin.site.register(Client)
admin.site.register(Employee)
