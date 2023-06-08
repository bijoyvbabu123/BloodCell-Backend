from django.shortcuts import render

import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class WebHookView(APIView):
    """
    =========response of /start
    {
    "update_id":734997090,
    "message":{
        "message_id":51,
        "from":{
            "id":996202131,
            "is_bot":false,
            "first_name":"Bijoy",
            "username":"bijoyvbabu123",
            "language_code":"en"
        },
        "chat":{
            "id":996202131,
            "first_name":"Bijoy",
            "username":"bijoyvbabu123",
            "type":"private"
        },
        "date":1686207037,
        "text":"/start YnZiMTIzbWlzY0BnbWFpbC5jb20=",
        "entities":[
            {
                "offset":0,
                "length":6,
                "type":"bot_command"
            }
        ]
    }
    }
    """
    def get(self, request, *args, **kwargs):
        print(request.data)
        encoded_email = request.data['message']['text'].split(' ')[1]
        print(encoded_email)
        print(base64.urlsafe_b64decode(encoded_email).decode())
        return Response(status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        print(request.data)
        encoded_email = request.data['message']['text'].split(' ')[1]
        print(encoded_email)
        print(base64.urlsafe_b64decode(encoded_email).decode())
        return Response(status=status.HTTP_200_OK)