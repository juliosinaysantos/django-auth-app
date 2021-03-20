from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from users.models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'is_superuser',
        'is_staff',
        'is_active'
    )
    fieldsets = (
        ('Account settings', {
            'fields': ('username', 'email', 'password')
        }),
        ('Status', {
            'fields': ('is_superuser', 'is_staff', 'is_active')
        }),
        ('Groups & Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions')
        }),
        ('Dates', {
            'fields': ('email_verified_at', 'created_at', 'updated_at', 'deleted_at', 'last_login')
        }),
        ('Tokens', {
            'fields': ('email_verification_token',)
        }),
    )
    add_fieldsets = (
        ('User', {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    readonly_fields = ('email_verification_token', 'created_at', 'updated_at', 'last_login')

    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
