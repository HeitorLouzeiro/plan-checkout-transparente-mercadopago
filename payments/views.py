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
    payment_methods_response = sdk.payment_methods().list_all()
    payment_methods = payment_methods_response["response"]
    return JsonResponse(payment_methods, safe=False)


def methodTicket(request):
    payment_data = {
        "transaction_amount": 100,
        "description": "Título do produto",
        # pec = Boleto Loterica, bolbradesco = Boleto Bradesco
        "payment_method_id": "bolbradesco",
        "payer": {
            "email": "UserTest@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "identification": {
                "type": "CPF",
                "number": "191191191-00"
            },
            "address": {
                "zip_code": "06233-200",
                "street_name": "Av. das Nações Unidas",
                "street_number": "3003",
                "neighborhood": "Bonfim",
                "city": "Osasco",
                "federal_unit": "SP"
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    return JsonResponse(payment, safe=False)
