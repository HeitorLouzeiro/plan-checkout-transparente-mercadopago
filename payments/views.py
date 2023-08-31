from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'payments/pages/home.html')


def checkout(request):
    return render(request, 'payments/pages/checkout.html')
