from django.contrib import admin

from .models import Payments, Product, Subscription

# Register your models here.

admin.site.register(Product)
admin.site.register(Payments)
admin.site.register(Subscription)
