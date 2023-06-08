from django.shortcuts import render

from rest_framework.generics import ListAPIView

import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .telegrambothandlerfunctions import (
    base_handler,
)
from .serializers import (
    UserTelegramDataSerializer,
)
from .models import (
    TelegramData,
)
from users.custompermissions import (
    IsAuthenticatedVerified,
)

# Create your views here.


class WebHookView(APIView):
    def get(self, request, *args, **kwargs):
        base_handler(request_data=request.data)
        return Response(status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        base_handler(request_data=request.data)
        return Response(status=status.HTTP_200_OK)
    

# user telegram profile fetch view
class UserTelegramData(APIView):
    permission_classes = [IsAuthenticatedVerified]
    serializer_class = UserTelegramDataSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_telegram_data = TelegramData.objects.get(user=user)
        serializer = self.serializer_class(user_telegram_data)
        return Response(serializer.data, status=status.HTTP_200_OK)