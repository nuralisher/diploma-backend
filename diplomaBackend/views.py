from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse

def hello(request):
    return JsonResponse([1, 3, 4], safe=False)