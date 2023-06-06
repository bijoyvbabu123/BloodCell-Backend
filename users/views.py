from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    ResendVerificationMailSerializer,
    ProfileUpdateSerializer,
)
from .utilities import (
    check_and_verify_user,
)
from .models import (
    User,
    Profile,
)
from .custompermissions import (
    IsAuthenticatedVerified,
    IsVerified,
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


# view to resend the verification mail
class ResendVerificationMailView(APIView):
    """
    resends the verification mail to the user.
    use this endpoint only if the user is not verified.
    returns status 200 with message if the mail is sent successfully.
    """

    serializer_class = ResendVerificationMailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        curr_user_email = serializer.validated_data['email']
        curr_user = User.objects.get(email=curr_user_email)

        # check if the user has verified their email and raise error if not
        if curr_user.is_email_verified:
            return Response({'email': ["Email is already verified."]}, status=status.HTTP_403_FORBIDDEN)
        
        # send the verification mail
        curr_user.send_verification_email(request=request)

        return Response({'email': ["Verification mail sent successfully."]}, status=status.HTTP_200_OK)


# view to update the user profile
class ProfileUpdateView(APIView):
    """
    Update the UserProfile instance of the user.
    Required fields in the request is clear from the serializer.
    Response is a success message with status code 200.
    """

    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticatedVerified]

    def post(self, request):
        curr_user = request.user
        curr_user_profile = Profile.objects.get(user=curr_user)

        serializer = self.serializer_class(curr_user_profile ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Profile updated successfully.'}, status=status.HTTP_200_OK)