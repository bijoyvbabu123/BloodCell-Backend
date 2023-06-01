from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import (
    SignUpSerializer,
)

# Create your views here.

class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # implement email verifcation here

        return Response(serializer.data, status=status.HTTP_201_CREATED)