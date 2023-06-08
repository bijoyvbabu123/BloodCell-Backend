from django.apps import AppConfig
from django.conf import settings

import requests

class TelegrambotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegrambot'

    def ready(self):

        url = settings.TELEGRAM_BOT_WEBHOOK_URL+"telebot/webhook/"
        token = settings.TELEGRAM_BOT_TOKEN
        payload = {
        'url': url
        }
        url = f'https://api.telegram.org/bot{token}/setWebhook'
        response = requests.post(url, data=payload)
        print(response.request.url)
        # Check the response status code
        if response.status_code == 200:
            print('webhooks set successfully !')
        else:
            print(f'Something went wrong: {response.status_code}')
