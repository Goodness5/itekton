from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CriticalFault

@receiver(post_save, sender=CriticalFault)
def update_critical_fault_status(sender, instance, **kwargs):
    current_datetime = timezone.now()

    if instance.expiration_date < current_datetime:
        instance.status = CriticalFault.Status.OVERDUE
    elif current_datetime < instance.expiration_date < (current_datetime + timezone.timedelta(days=30)):
        instance.status = CriticalFault.Status.SOON
    else:
        instance.status = CriticalFault.Status.COMPLETED

    instance.save()
