from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Payments, Product, Subscription


@receiver(post_save, sender=Payments)
def create_subscription(sender, instance, **kwargs):
    if instance.status == 'approved':
        Subscription.objects.create(
            user=instance.user,
            product=instance.product,
            payments=instance,  # Use a relação 'payments' para associar Payments a Subscription
            date_of_expiration=instance.date_of_expiration,
            status='Active'
        )
