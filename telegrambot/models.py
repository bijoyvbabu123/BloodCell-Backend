from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class TelegramData(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='telegramdata',
    )
    telegram_verification_link = models.CharField(
        _('telegram verification link'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Add your telegram verification link.'),
        error_messages={
            'max_length': _('Telegram verification link is too long.'),
        }
    )
    chat_id = models.CharField(
        _('chat id'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Add your chat id.'),
        error_messages={
            'max_length': _('Chat id is too long.'),
        }
    )
    is_telegram_verified = models.BooleanField(
        _('telegram verified status'),
        default = False,
        help_text=_('Designates whether this user has verified their telegram.'),
    )
    