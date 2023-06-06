from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    TelegramData,
)
from users.models import (
    User,
)


# creating TelegramData instance for new user
@receiver(post_save, sender=User)
def create_telegram_profile(sender, instance, created, **kwargs):
    if created:
        TelegramData.objects.create(user=instance)
    
