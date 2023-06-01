from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import (
    SignUpSerializer,
)
from .utilities import (
    check_and_verify_user,
)

import jwt

# Create your views here.

class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        curr_user = serializer.save()

        curr_user.send_verification_email(request=request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    """
    email verification using the token as a query parameter
    """
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            check_and_verify_user(pkey=payload['user_id'])
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
