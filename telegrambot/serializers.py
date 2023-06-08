from rest_framework import serializers

from .models import TelegramData



class UserTelegramDataSerializer(serializers.ModelSerializer):
    user_mail = serializers.SerializerMethodField()
    class Meta:
        model = TelegramData
        fields = (
            'user_mail',
            'telegram_verification_link',
            'chat_id',
            'is_telegram_verified',
        )
        read_only_fields = (
            'user_mail',
            'telegram_verification_link',
            'chat_id',
            'is_telegram_verified',
        )

    def get_user_mail(self, obj):
        return obj.user.email
