from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from . import models

@receiver(post_save, sender=User)
def create_user_stats_model(sender, instance, created, **kwargs):
    if created:
        models.UserStatsModel.objects.create(user=instance)
        
