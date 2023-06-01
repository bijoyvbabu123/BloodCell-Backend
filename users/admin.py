from django.contrib import admin

from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_email_verified', 'date_joined', 'is_active', 'is_staff')
    list_filter = ('is_email_verified', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'date_joined')
    ordering = ('email',)





admin.site.register(User, UserAdmin)
