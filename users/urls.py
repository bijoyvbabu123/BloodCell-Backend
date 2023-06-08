from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    SignUpView,
    VerifyEmail,
    LoginView,
    ResendVerificationMailView,
    ProfileUpdateView,
    ProfileDataView,
)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'), # user signup
    path('verifyemail/', VerifyEmail.as_view(), name='verifyemail'), # email verification
    path('login/', LoginView.as_view(), name='login'), # user login
    path('resend-verification-mail/', ResendVerificationMailView.as_view(), name='resend-verification-mail'), # resend verification mail
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # token refresh
    path('profileupdate/', ProfileUpdateView.as_view(), name='profileupdate'), # profile update
    path('getprofiledata/', ProfileDataView.as_view(), name='getprofiledata'), # get profile data
]