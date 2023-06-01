from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy as _

from .models import User


class SignUpSerializer(serializers.Serializer):
    
    email = serializers.EmailField(
        max_length=255,
        required=True,
        allow_blank=False,
        allow_null=False,
        help_text='Required. Add a valid email address.',
        error_messages={
            'required': 'Email is required.',
            'blank': 'Email is required.',
            'null': 'Email is required.',
            'invaild': 'Please enter a valid email Address',
        },
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), 
                message=_('User with this email already exists')
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        max_length=128,
        required=True,
        allow_blank=False,
        allow_null=False,
        help_text='Required. Add a valid password.',
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password is required.',
            'null': 'Password is required.',
        },
    )


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        return attrs
    
    def create(self, validated_data):
        email = validated_data.get('email', '')
        password = validated_data.get('password', '')
        return User.objects.create_user(email=email, password=password)
    