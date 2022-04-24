from django.urls import path

from user_management.views import ClientRegistrationView, EmployeeRegistrationView

urlpatterns = [
    path('client/registration/', ClientRegistrationView.as_view()),
    path('employee/registration/', EmployeeRegistrationView.as_view()),
]
