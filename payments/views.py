import json
import os
from datetime import datetime

import mercadopago
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from .models import Product

sdk = mercadopago.SDK(os.environ.get('ACCESS_TOKEN'))


# Create your views here.


def home(request):
    template_name = 'payments/pages/home.html'
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name, context)


def checkout(request):
    if request.method == 'GET':
        plan = request.GET.get('sub_plan')
        fetch_plan = Product.objects.get(name=plan)

        if not fetch_plan:
            return HttpResponseNotFound()

    response = {}
    if request.method == 'POST':
        fistname = request.POST.get('fistname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cpf = request.POST.get('cpf')
        methodpayment = request.POST.get('paymentMethod')
        amount = request.POST.get('plan')
        try:
            amount = float(amount)
            fetch_plan = Product.objects.get(price=amount)
        except Product.DoesNotExist:
            return HttpResponseNotFound()

        response = {
            'fistname': fistname,
            'lastname': lastname,
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

    context = {
        'plan': fetch_plan
    }

    return render(request, 'payments/pages/checkout.html', context)


def paymentsConfirm(request):
    # Retrieve the JSON data from the session
    checkout_data_json = request.session.get('checkout_data', None)
    if not checkout_data_json:
        return HttpResponseNotFound()

    if checkout_data_json:
        # Parse the JSON data
        checkout_data = json.loads(checkout_data_json)

    # Pass the data to the template context
    context = {'checkout_data': checkout_data}

    return render(request, 'payments/pages/paymentsConfirm.html', context)


def payment(request):
    if request.method == 'GET':
        return HttpResponseNotFound()

    if request.method == 'POST':
        checkout_data_json = request.session.get('checkout_data', None)
        checkout_data = json.loads(checkout_data_json)

        fistname = checkout_data['fistname']
        lastname = checkout_data['lastname']
        email = checkout_data['email']
        cpf = checkout_data['cpf']
        methodpayment = checkout_data['methodpayment']
        amount = checkout_data['amount']

        if methodpayment == 'boleto':
            methodpayment = 'bolbradesco'

        payment_data = {
            "transaction_amount": amount,
            "description": "Título do produto",
            "payment_method_id": methodpayment,
            "payer": {
                "email": email,
                "first_name": fistname,
                "last_name": lastname,
                "identification": {
                    "type": "CPF",
                    "number": cpf
                }
            }
        }

        payment_response = sdk.payment().create(payment_data)

        # Mercado Pago response
        payment = payment_response["response"]

        checkout_data = request.session.clear()

        # converting date
        data_expire = payment['date_of_expiration']
        data_format = datetime.fromisoformat(data_expire)
        data_format = data_format.strftime('%d/%m/%Y %H:%M:%S')

        context = {
            'payment': payment,
            'data_expire': data_format,
        }
        return render(request, 'payments/pages/payment.html', context)
