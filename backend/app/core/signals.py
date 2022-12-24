from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TelemetryData


@receiver(post_save, sender=TelemetryData)
def update_last_answer(sender, instance, **kwargs):
    created = kwargs.get("created", False)
    raw = kwargs.get("raw", False)
    if created and not raw:
        TelemetryData.objects.filter(author=instance.author, exercise=instance.exercise).exclude(id=instance.id).update(last=False)
