from django.urls import path

from .views import (
    WebHookView,
)


urlpatterns = [
    path('webhook/', WebHookView.as_view(), name='webhook'),
]