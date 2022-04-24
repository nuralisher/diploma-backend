from django.contrib.auth.models import User
from django.db import models



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Employee(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
