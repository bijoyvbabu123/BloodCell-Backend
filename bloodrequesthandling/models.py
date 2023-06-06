from django.db import models

from users.hardcodedata import (
    district_choices,
    blood_group_choices,
)

from datetime import date



# Create your models here.

class BloodRequirement(models.Model):
    blood_group = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        help_text='Blood Group required.',
        choices=blood_group_choices,
    )
    name_of_patient = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text='Name of patient.',
    )
    date_of_donation = models.DateField(
        blank=False,
        null=False,
        help_text='Donation Date.',
    )
    donation_venue = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text='Donation venue.',
    )
    district = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text='District.',
        choices=district_choices,
    )
    contact_number = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        help_text='Contact number of the patient of by-stander.',
    )
    patient_case = models.TextField(
        blank=False,
        null=False,
        help_text='Patient case.',
    )
    additional_info = models.TextField(
        blank=True,
        null=True,
        help_text='Add any additional information if any.',
    )
    no_of_units = models.IntegerField(
        blank=False,
        null=False,
        help_text='Number of units required.',
    )
    is_case_verified = models.BooleanField(
        default=None,
        blank=True,
        null=True,
        help_text='Is case verified by admin. (True/False) after admin verification. None if admin has not yet verified.',
    )
    date_of_request = models.DateField(
        auto_now_add=True,
        blank=False,
        null=False,
        help_text='Date of request.',
    )

    def __str__(self):
        return self.name_of_patient + ' - ' + self.blood_group
    
    class Meta:
        verbose_name = 'Blood Requirement'
        verbose_name_plural = 'Blood Requirements'
    
    def is_case_live(self):
        # return True if the date_of_donation is greater than or equal to today's date
        return self.date_of_donation > date.today()


# model for available donors for each requirements
class AvailableDonors(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='User.',
    )
    blood_requirement = models.ForeignKey(
        'BloodRequirement',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Blood requirement.',
    )
    is_willing_to_donate = models.BooleanField(
        default=None,
        blank=True,
        null=True,
        help_text='Is willing to donate. (True/False) after user confirmation. None if user has not yet confirmed.',
    )
    approved_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Time when the user gave a response to the request.',
    )

    def __str__(self):
        return self.user.email + ' - ' + self.blood_requirement.name_of_patient
    
    class Meta:
        verbose_name = 'Available Donor'
        verbose_name_plural = 'Available Donors'
    

# completed donations
class CompletedDonations(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='User.',
    )
    blood_requirement = models.ForeignKey(
        'BloodRequirement',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Blood requirement.',
    )
    is_user_verified = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        help_text='Has the user verified the donation has been completed. (True/False) after user verification.',
    )
    is_admin_verified = models.BooleanField(
        default=None,
        blank=True,
        null=True,
        help_text='Has the admin verified the donation has been completed. (True/False) after admin verification. None if admin has not yet verified.',
    )

    def __str__(self):
        return self.user.email + ' - ' + self.blood_requirement.name_of_patient
    
    class Meta:
        verbose_name = 'Completed Donation'
        verbose_name_plural = 'Completed Donations'

    
