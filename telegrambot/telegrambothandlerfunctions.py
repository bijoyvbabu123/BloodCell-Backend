import base64

from users.models import (
   User,
)
from .models import (
   TelegramData,
)



# assign chat_id and set is_telegram_verified to True for the user
def assign_chat_id_and_verified_status(email, chat_id):
   if User.objects.filter(email=email).exists():
      user = User.objects.get(email=email)
      user_telegram_data = TelegramData.objects.get(user=user)
      user_telegram_data.chat_id = chat_id
      user_telegram_data.is_telegram_verified = True
      user_telegram_data.save()


# /start command handler function
def start_command_handler(request_data):
   encoded_email = request_data['message']['text'].split(' ')[1]
   decoded_email = base64.urlsafe_b64decode(encoded_email).decode()
   chat_id = str(request_data['message']['chat']['id'])
   assign_chat_id_and_verified_status(email=decoded_email, chat_id=chat_id)


# main handler function
def base_handler(request_data):
   print(request_data)
    
   if 'message' in request_data and 'entities' in request_data['message']:
      if request_data['message']['entities'][0]['type'] == 'bot_command':
         if request_data['message']['text'].split(' ')[0] == '/start':
            start_command_handler(request_data)
