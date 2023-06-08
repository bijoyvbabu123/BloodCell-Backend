from django.urls import path

from .views import (
    WebHookView,
    UserTelegramData,
)


urlpatterns = [
    path('webhook/', WebHookView.as_view(), name='webhook'), # webhook url
    path('userdata/', UserTelegramData.as_view(), name='userdata'), # user telegram data
]