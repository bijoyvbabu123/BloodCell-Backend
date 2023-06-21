from django.urls import path

from .views import (
    FindBlood,
    LiveRequirements,
)



urlpatterns = [
    path('findblood/', FindBlood.as_view(), name='findblood'), # find_blood endpoint
    path('liverequirements/', LiveRequirements.as_view(), name='liverequirements'), # live_requirements endpoint
]