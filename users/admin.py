from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.html import format_html
from django.urls import reverse


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'mobile_number', 'picture')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    list_display = (
        'username',
        'email',
        'mobile_number',
        'is_staff',
        'is_active',
        'change_password_button'
    )

    def change_password_button(self, obj):
        return format_html(
            '<a class="btn btn-warning btn-sm" href="/api/admin/users/customuser/{}/password/">Change Password</a>',
            obj.pk
        )

   
admin.site.register(CustomUser, CustomUserAdmin)