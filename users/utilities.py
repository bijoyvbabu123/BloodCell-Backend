from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.apps import apps

import threading



# returns the absolute url for the email verification link, given the request and the token
def get_abs_verification_url(request, token):
    current_site = get_current_site(request).domain
    relative_link = reverse('verifyemail')
    abs_url = 'http://' + current_site + relative_link + '?token=' + str(token)
    return abs_url

# creates verification email for the user
def create_verification_email(request, user, token):
    nl = '\n'
    email_subject = 'Blood Cell Email Verification'
    email_body = f'Hello {user.email} {nl} Please verify your email by clicking on the link below {nl} {get_abs_verification_url(request, token)}'
    to_email = user.email

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=[to_email]
    )

    return email

# sends the verification email to the user
class EmailUtil:
    @staticmethod
    def send_email(email):
        EmailThread(email).start()

# email threading
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# veriy the user, given the primarykey
def check_and_verify_user(pkey):
    User = apps.get_model('users', 'User')
    user = User.objects.get(pk=pkey)
    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()