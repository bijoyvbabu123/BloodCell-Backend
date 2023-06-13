from django.urls import path

from .views import (
    FindBlood,
)



urlpatterns = [
    path('findblood/', FindBlood.as_view(), name='findblood'), # find_blood endpoint
]