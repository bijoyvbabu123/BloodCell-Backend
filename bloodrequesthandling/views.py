from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import (
    FindBloodSerializer,
    LiveRequirementsSerializer,
)
from .models import (
    BloodRequirement,
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
    

class LiveRequirements(generics.ListAPIView):
    queryset = BloodRequirement.get_live_verified_cases()
    serializer_class = LiveRequirementsSerializer