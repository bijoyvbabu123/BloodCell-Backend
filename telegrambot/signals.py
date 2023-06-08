from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import (
    TelegramData,
)
from users.models import (
    User,
)
from .messagetemplates import (
    v_link,
)



# creating TelegramData instance for new user
@receiver(post_save, sender=User)
def create_telegram_profile(sender, instance, created, **kwargs):
    if created:
        telegram_profile = TelegramData.objects.create(user=instance)
        verification_link = v_link.format(
            v_link_bot_username=settings.TELEGRAM_BOT_USERNAME,
            v_link_parameter=instance.get_email_base64url(),
        )
        telegram_profile.telegram_verification_link = verification_link
        telegram_profile.save()


    
