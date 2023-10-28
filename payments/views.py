import json
import os
from datetime import datetime

import mercadopago
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from .models import Payments, Product

sdk = mercadopago.SDK(os.environ.get('ACCESS_TOKEN'))


# Create your views here.


def home(request):
    template_name = 'payments/pages/home.html'
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name, context)


def checkout(request):

    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.info(request, 'You need to login first')

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
            'amount': amount,
            'nameplan': fetch_plan.name,
        }
        # Store the response data in the session
        request.session['checkout_data'] = json.dumps(response)

        # Redirect to the 'payments' view
        return redirect('payments:paymentsConfirm')

    context = {
        'plan': fetch_plan
    }

    return render(request, 'payments/pages/checkout.html', context)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
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


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
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
        plan = checkout_data['nameplan']
        amount = checkout_data['amount']

        if methodpayment == 'boleto':
            methodpayment = 'bolbradesco'

        payment_data = {
            "transaction_amount": amount,
            "description": plan,
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

        product = Product.objects.get(name=plan)

        paymentsave = Payments(
            first_name=payment["payer"]["first_name"],
            last_name=payment["payer"]["last_name"],
            email=payment["payer"]["email"],
            idetification_type=payment["payer"]["identification"]["type"],
            idetification_number=payment["payer"]["identification"]["number"],
            payment_id=payment["id"],
            description=payment["description"],
            date_approved=payment["date_approved"],
            date_of_expiration=payment["date_of_expiration"],
            date_last_updated=payment["date_last_updated"],
            payment_method_id=payment["payment_method_id"],
            status=payment["status"],
            amount=payment["transaction_amount"],
            user=request.user,
            product_id=product.id,
        )
        paymentsave.save()

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
