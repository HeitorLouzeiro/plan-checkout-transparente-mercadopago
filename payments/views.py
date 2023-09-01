import json
import os

import mercadopago
from django.http import JsonResponse
from django.shortcuts import redirect, render

sdk = mercadopago.SDK(os.environ.get('ACCESS_TOKEN'))


# Create your views here.


def home(request):
    return render(request, 'payments/pages/home.html')


def checkout(request):
    response = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cpf = request.POST.get('cpf')
        methodpayment = request.POST.get('paymentMethod')
        amount = 100

        response = {
            'name': name,
            'email': email,
            'phone': phone,
            'cpf': cpf,
            'methodpayment': methodpayment,
            'amount': amount
        }
        # Store the response data in the session
        request.session['checkout_data'] = json.dumps(response)

        # Redirect to the 'payments' view
        return redirect('paymentsConfirm')
    return render(request, 'payments/pages/checkout.html')


def paymentsConfirm(request):

    # Retrieve the JSON data from the session
    checkout_data_json = request.session.get('checkout_data', None)

    if checkout_data_json:
        # Parse the JSON data
        checkout_data = json.loads(checkout_data_json)
    else:
        # Handle the case where the data is not found in the session
        checkout_data = {}
        return redirect('paymentsCheckout')

    # Pass the data to the template context
    context = {'checkout_data': checkout_data}

    return render(request, 'payments/pages/paymentsConfirm.html', context)


def payment(request):
    return render(request, 'payments/pages/payment.html')


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


def methodPix(request):
    payment_data = {
        "transaction_amount": 100,
        "description": "Título do produto",
        "payment_method_id": "pix",
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
