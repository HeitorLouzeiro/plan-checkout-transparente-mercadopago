from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Product(models.Model):
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period_duration = models.CharField(
        max_length=10, choices=PERIOD_DURATION, default='Days')
    duration = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Payments(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100)
    idetification_type = models.CharField(max_length=10)
    idetification_number = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=11)
    description = models.CharField(max_length=100)
    date_approved = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_expiration = models.DateTimeField(null=True, blank=True)
    date_last_updated = models.DateTimeField(null=True, blank=True)
    payment_method_id = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.email + " - " + self.payment_id + " - " + self.status


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    payments = models.ForeignKey(
        Payments, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True, blank=True)
    date_of_expiration = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return self.user.username + " - " + self.product.name + " - " + self.status
