from django.contrib import admin

# Register your models here.

from .models import (
    BloodRequirement,
    AvailableDonors,
    CompletedDonations,
)

class BloodRequirementAdmin(admin.ModelAdmin):
    list_display = ('name_of_patient', 'blood_group', 'date_of_donation', 'contact_number', 'no_of_units', 'is_case_verified')
    list_filter = ('blood_group', 'district', 'is_case_verified')
    search_fields = ('name_of_patient', 'blood_group', 'date_of_donation', 'contact_number', 'no_of_units', 'is_case_verified')
    ordering = ('-date_of_request',)


class AvailableDonorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_requirement', 'is_willing_to_donate')
    list_filter = ('is_willing_to_donate', 'blood_requirement__blood_group')
    search_fields = ('user', 'blood_requirement', 'is_willing_to_donate')
    ordering = ('user',)


class CompletedDonationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_requirement', 'is_user_verified', 'is_admin_verified')
    list_filter = ('is_user_verified', 'is_admin_verified', 'user')
    search_fields = ('user', 'blood_requirement')
    ordering = ('user',)


admin.site.register(BloodRequirement, BloodRequirementAdmin)
admin.site.register(AvailableDonors, AvailableDonorsAdmin)
admin.site.register(CompletedDonations, CompletedDonationsAdmin)

