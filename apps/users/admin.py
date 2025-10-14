from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User, Region, PhoneVerification


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'code', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['phone_number']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone_number', 'first_name', 'last_name', 'region', 'is_phone_verified', 'is_active']
    list_filter = ['is_phone_verified', 'is_active', 'is_staff', 'region']
    search_fields = ['phone_number', 'first_name', 'last_name']
    ordering = ['phone_number']
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'region')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительно', {'fields': ('is_phone_verified', 'terms_accepted')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2', 'region', 'terms_accepted'),
        }),
    )
