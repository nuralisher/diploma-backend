from django.contrib.auth.models import User
from django.db import models



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Employee(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
