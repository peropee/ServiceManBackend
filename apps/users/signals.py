from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ClientProfile, ServicemanProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'CLIENT':
            ClientProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'SERVICEMAN':
            ServicemanProfile.objects.get_or_create(user=instance)