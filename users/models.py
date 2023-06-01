from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager


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