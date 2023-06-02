from django.urls import path

from .views import (
    SignUpView,
    VerifyEmail,
    LoginView,
    ResendVerificationMailView,
)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'), # user signup
    path('verifyemail/', VerifyEmail.as_view(), name='verifyemail'), # email verification
    path('login/', LoginView.as_view(), name='login'), # user login
    path('resend-verification-mail/', ResendVerificationMailView.as_view(), name='resend-verification-mail'), # resend verification mail
]