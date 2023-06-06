from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.utils.translation import gettext_lazy as _

from .models import User
from .hardcodedata import (
    blood_group_choices,
    district_choices,
)


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


class LoginSerializer(serializers.Serializer):
    """
    request : email, password (both char fields; required; in body)
    only for input purpose.
    email validation ( if the entered mail id exists )
    """
    email = serializers.EmailField(
        required=True,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        write_only_fields = ['password', 'email']
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exists")
        return value


# resend verification mail serializer
class ResendVerificationMailSerializer(serializers.Serializer):
    """
    request : email (char field; required; in body)
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exists")
        return value


# profile update serializer
class ProfileUpdateSerializer(serializers.Serializer):

    first_name = serializers.CharField(
        max_length=30,
    )
    last_name = serializers.CharField(
        max_length=30,
    )
    phone_number = serializers.CharField(
        max_length=10,
    )
    address = serializers.CharField(
        max_length=225,
    )
    district = serializers.ChoiceField(
        choices=district_choices,
    )
    pincode = serializers.CharField(
        max_length=6,
    )
    dateofbirth = serializers.DateField(
    )
    blood_group = serializers.ChoiceField(
        choices=blood_group_choices,
    )
    last_donated_on = serializers.DateField(
        required=False,
    )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.district = validated_data.get('district', instance.district)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.dateofbirth = validated_data.get('dateofbirth', instance.dateofbirth)
        instance.blood_group = validated_data.get('blood_group', instance.blood_group)
        instance.last_donated_on = validated_data.get('last_donated_on', instance.last_donated_on)
        instance.save()
        return instance

