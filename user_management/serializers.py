from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
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

    def get_cleaned_data(self):
        data = super(EmployeeRegistrationSerializer, self).get_cleaned_data()
        extra_data = {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }
        data.update(extra_data)
        return data

    def save(self, request):
        user = super(EmployeeRegistrationSerializer, self).save(request)
        user.is_employee = True
        user.save()
        employee = Employee(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'))
        employee.save()
        return user


class RestaurantsEmployeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'user_id')
