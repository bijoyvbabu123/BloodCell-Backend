from rest_framework import serializers

from users.hardcodedata import (
    blood_group_choices,
    district_choices,
)
from .models import (
    BloodRequirement,
)



class FindBloodSerializer(serializers.Serializer):
    blood_group = serializers.ChoiceField(
        choices=blood_group_choices,
        help_text='Blood Group required.',
        allow_blank=False,
        allow_null=False,
    )
    name_of_patient = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        help_text='Name of patient.',
        max_length=255,
    )
    date_of_donation = serializers.DateField(
        help_text='Donation Date.',
    )
    donation_venue = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        help_text='Donation venue.',
        max_length=255,
    )
    district = serializers.ChoiceField(
        choices=district_choices,
        help_text='District.',
        allow_blank=False,
        allow_null=False,
    )
    contact_number = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        help_text='Contact number of the patient or by-stander.',
        max_length=15,
    )
    patient_case = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        help_text='Patient case.',
    )
    additional_info = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        help_text='Add any additional information if any.',
        required=False,
    )
    no_of_units = serializers.IntegerField(
        help_text='Number of units required.',
    )

    def create(self, validated_data):
        return BloodRequirement.objects.create(
            blood_group=validated_data['blood_group'],
            name_of_patient=validated_data['name_of_patient'],
            date_of_donation=validated_data['date_of_donation'],
            donation_venue=validated_data['donation_venue'],
            district=validated_data['district'],
            contact_number=validated_data['contact_number'],
            patient_case=validated_data['patient_case'],
            # additional_info=validated_data['additional_info'],
            additional_info=validated_data.get('additional_info', None),
            no_of_units=validated_data['no_of_units'],
        )
