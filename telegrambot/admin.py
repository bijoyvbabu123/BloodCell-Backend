from django.contrib import admin

# Register your models here.

from .models import (
    TelegramData,
)

class TelegramDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_telegram_verified', 'chat_id', 'telegram_verification_link')
    list_filter = ('is_telegram_verified',)
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name', 'chat_id')
    ordering = ('user',)



admin.site.register(TelegramData, TelegramDataAdmin)
