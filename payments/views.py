import os

import mercadopago
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

sdk = mercadopago.SDK(os.environ.get('ACCESS_TOKEN'))


# Create your views here.


def home(request):
    return render(request, 'payments/pages/home.html')


def checkout(request):
    return render(request, 'payments/pages/checkout.html')


def methodsPayments(request):
    print(sdk)
    payment_methods_response = sdk.payment_methods().list_all()
    payment_methods = payment_methods_response["response"]
    return JsonResponse(payment_methods, safe=False)
