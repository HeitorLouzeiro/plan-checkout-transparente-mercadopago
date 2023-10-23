from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('payments-confirm/', views.paymentsConfirm, name='paymentsConfirm'),
    path('payment/', views.payment, name='payment'),
]
