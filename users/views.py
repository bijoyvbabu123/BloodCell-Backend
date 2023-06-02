from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import (
    SignUpSerializer,
    LoginSerializer,
)
from .utilities import (
    check_and_verify_user,
)
from .models import (
    User,
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


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        curr_user_email = serializer.validated_data['email']
        curr_user = User.objects.get(email=curr_user_email)

        # check if the user has verified their email and raise error if not
        if not curr_user.is_email_verified:
            return Response({'email': ["Email is not verified."]}, status=status.HTTP_403_FORBIDDEN)
        
        # authenticate the user and return the tokens
        auth_user = authenticate(email=curr_user_email, password=serializer.validated_data['password'])
        if auth_user is not None:
            tokens = auth_user.generate_tokens()
            return Response(tokens, status=status.HTTP_200_OK)


        return Response({'password': ["Wrong Password"]}, status=status.HTTP_400_BAD_REQUEST)