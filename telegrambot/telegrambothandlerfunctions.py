import base64
import requests
import json
import threading

from django.conf import settings

from users.models import (
   User,
)
from .models import (
   TelegramData,
)
from .messagetemplates import (
   welcome_message,
   blood_req_body,
)

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN



class BloodRequestThread(threading.Thread):
   def __init__(self, chat_ids, blood_req, message, reply_markup):
      self.chat_ids = chat_ids
      self.blood_req = blood_req
      self.message = message
      self.reply_markup = reply_markup
      threading.Thread.__init__(self)

   def run(self):
      for chat_id in self.chat_ids:
         payload = {
            "chat_id": chat_id,
            "text": self.message,
            "reply_markup": json.dumps(self.reply_markup),
         }
         send_message_endpoint = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage'
         response = requests.post(send_message_endpoint, data=payload)


class BloodRequestMessage():
   # send blood request message to users
   @staticmethod
   def send_blood_request_messages(chat_ids, blood_req):
      
      message = blood_req_body.format(
         name_of_patient=blood_req.name_of_patient,
         blood_group=blood_req.blood_group,
         date_of_donation=blood_req.date_of_donation,
         donation_venue=blood_req.donation_venue,
         district=blood_req.district,
         contact_number=blood_req.contact_number,
         no_of_units=blood_req.no_of_units,
         patient_case=blood_req.patient_case,
         additional_info=blood_req.additional_info,
      )

      # call back slit by $ ['bloodcell', 'yes', '{id}']
      yes_button = {
         "text": "Yes, I'm willing to donate",
         "callback_data": "bloodcell$yes$"+str(blood_req.id),
      }
      no_button = {
         "text": "No, I'm having other commitments",
         "callback_data": "bloodcell$no$"+str(blood_req.id),
      }
      inline_keyboard = [[yes_button], [no_button]]
      reply_markup = {
         "inline_keyboard": inline_keyboard
      }

      BloodRequestThread(chat_ids=chat_ids, blood_req=blood_req, message=message, reply_markup=reply_markup).start()

# send a message to the user
def send_message(chat_id, message):
   send_message_endpoint = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message
   response = requests.get(send_message_endpoint)
   print(response)



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
   try:
      encoded_email = request_data['message']['text'].split(' ')[1]
      decoded_email = base64.urlsafe_b64decode(encoded_email).decode()
      chat_id = str(request_data['message']['chat']['id'])
      assign_chat_id_and_verified_status(email=decoded_email, chat_id=chat_id)
      send_message(chat_id=chat_id, message=welcome_message)
   except:
      pass


# main handler function
def base_handler(request_data):
   print(request_data)
    
   if 'message' in request_data and 'entities' in request_data['message']:
      if request_data['message']['entities'][0]['type'] == 'bot_command':
         if request_data['message']['text'].split(' ')[0] == '/start':
            start_command_handler(request_data)
