from django.urls import path

from .views import (
    SignUpView,
    VerifyEmail,
    LoginView,
)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'), # user signup
    path('verifyemail/', VerifyEmail.as_view(), name='verifyemail'), # email verification
    path('login/', LoginView.as_view(), name='login'), # user login
]