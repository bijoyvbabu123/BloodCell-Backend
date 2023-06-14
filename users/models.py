from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

from datetime import date, timedelta

import base64

from .managers import UserManager
from .utilities import (
    create_verification_email,
    EmailUtil,
)
from .hardcodedata import (
    district_choices,
    blood_group_choices,
)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. Add a valid email address.'),
        error_messages={
            'unique': _('A user with that email already exists.'),
            'required': _('Email is required.'),
            'blank': _('Email is required.'),
            'null': _('Email is required.'),
            'invaild': _('Please enter a valid email Address'),
        }
    )
    is_email_verified = models.BooleanField(
        _('email verified status'),
        default = False,
        help_text=_('Designates whether this user has verified their email.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('email',)

    def __str__(self):
        return self.email

    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def send_verification_email(self, request):
        access_token = self.generate_tokens()['access']
        v_mail = create_verification_email(request=request, user=self, token=access_token)
        EmailUtil.send_email(v_mail)
    
    def get_email_base64url(self):
        encoded_email = base64.urlsafe_b64encode(self.email.encode()).decode()
        return encoded_email


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('Add your first name.'),
        error_messages={
            'max_length': _('First name is too long.'),
        }
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        null=True,
        help_text=_('Add your last name.'),
        error_messages={
            'max_length': _('Last name is too long.'),
        }
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True,
        null=True,
        help_text=_('Add your phone number.'),
        error_messages={
            'max_length': _('Phone number is too long.'),
        }
    )
    address = models.CharField(
        _('address'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Add your address.'),
        error_messages={
            'max_length': _('Address is too long.'),
        }
    )
    district = models.CharField(
        _('district'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Add your district.'),
        error_messages={
            'max_length': _('District is too long.'),
        },
        choices=district_choices,
    )
    pincode = models.CharField(
        _('pincode'),
        max_length=6,
        blank=True,
        null=True,
        help_text=_('Add your pincode.'),
        error_messages={
            'max_length': _('Pincode is too long.'),
        }
    )
    dateofbirth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True,
        help_text=_('Add your date of birth.'),
    )
    blood_group = models.CharField(
        _('blood group'),
        max_length=3,
        blank=True,
        null=True,
        help_text=_('Add your blood group.'),
        error_messages={
            'max_length': _('Blood group is too long.'),
        },
        choices=blood_group_choices,
    )
    last_donated_on = models.DateField(
        _('last donated on'),
        blank=True,
        null=True,
        help_text=_('Add your last donated on.'),
    )

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        ordering = ('user__email',)
    
    def __str__(self):
        if self.blood_group:
            return self.user.email+self.blood_group
        else:
            return self.user.email+"--"
    
    def get_full_name(self):
        return self.first_name+' '+self.last_name
    
    def get_age(self):
        today = date.today()
        age = today.year - self.dateofbirth.year
        if today.month < self.dateofbirth.month or (today.month == self.dateofbirth.month and today.day < self.dateofbirth.day):
            age -= 1
        return age
    
    def is_three_months_past_last_donation(self):
        today = date.today()
        three_months_ago = today - timedelta(days=90)
        if self.last_donated_on:
            if self.last_donated_on < three_months_ago:
                return True
        return False
    
    def is_date_three_months_past_last_donation(self, comp_date):
        three_months_ago = comp_date - timedelta(days=90)
        if self.last_donated_on:
            if self.last_donated_on < three_months_ago:
                return True
        return False

    def is_profile_complete(self):
        check = True
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'district', 'pincode', 'dateofbirth', 'blood_group']
        for field in fields:
            if getattr(self, field) is None or getattr(self, field) == '':
                check = False
                break
        return check
