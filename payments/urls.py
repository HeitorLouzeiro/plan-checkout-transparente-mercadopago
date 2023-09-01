from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('methods-payments/', views.methodsPayments, name='methodsPayments'),
    path('method-ticket/', views.methodTicket, name='methodTicket'),
]
