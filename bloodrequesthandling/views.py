from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    FindBloodSerializer,
)

# Create your views here.


class FindBlood(APIView):
    serializer_class = FindBloodSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data) ############################################
        return Response(serializer.data, status=status.HTTP_201_CREATED)