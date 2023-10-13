from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Payments, Product, Subscription


@receiver(post_save, sender=Payments)
def create_subscription(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product.id)
    duration_in_days = product.duration_in_days()
    date_of_expiration = timezone.now() + timedelta(days=duration_in_days)
    if instance.status == 'approved':
        Subscription.objects.create(
            user=instance.user,
            product=instance.product,
            # Use the 'payments' relationship to associate Payments with Subscription
            payments=instance,
            date_of_expiration=date_of_expiration,
            status='Active'
        )


@receiver(post_save, sender=Subscription)
def update_subscription(sender, instance, **kwargs):
    if instance.date_of_expiration < timezone.now() and instance.status != 'Inactive':
        subscription = Subscription.objects.get(id=instance.id)
        subscription.date_last_updated = timezone.now()
        subscription.status = 'Inactive'
        subscription.save()
