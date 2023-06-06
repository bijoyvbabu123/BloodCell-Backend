from django.contrib import admin

from .models import (
    User, 
    Profile,
)

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_email_verified', 'date_joined', 'is_active', 'is_staff')
    list_filter = ('is_email_verified', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'date_joined')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'blood_group')
    list_filter = ('blood_group',)
    search_fields = ('user', 'first_name', 'last_name', 'phone_number', 'blood_group')
    ordering = ('user',)




admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)