from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

from user_management.models import Client, Employee


class ClientRegistrationSerializer(RegisterSerializer):

    def save(self, request):
        user = super(ClientRegistrationSerializer, self).save(request)
        user.is_client = True
        user.save()
        client = Client(user=user)
        client.save()
        return user

class EmployeeRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def save(self, request):
        user = super(EmployeeRegistrationSerializer, self).save(request)
        user.is_employee = True
        user.save()
        employee = Employee(user=user)
        employee.save()
        return user

