from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

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

    def duration_in_days(self):
        if self.period_duration == 'Days':
            return self.duration
        elif self.period_duration == 'Months':
            return self.duration * 30  # Assuming 30 days in a month
        elif self.period_duration == 'Years':
            return self.duration * 365  # Assuming 365 days in a year
        else:
            return None  # Handle invalid duration gracefully

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def statusApproved(self):
        if self.status == 'pending':
            self.status = 'approved'
            self.date_approved = datetime.now()
            self.date_last_updated = datetime.now()
            self.save()

    def __str__(self):
        return self.email + " - " + self.payment_id + " - " + self.status


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    payments = models.ForeignKey(
        Payments, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(null=True, blank=True)
    date_of_expiration = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Inactive')

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        createdata = self.date_created.strftime("%d/%m/%Y")
        dateExpire = self.date_of_expiration.strftime("%d/%m/%Y")
        return self.user.username + " - " + self.product.name + " - " \
            + createdata + " - " + self.status + " - " + dateExpire
