from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Shipping


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'auth_provider', 'is_staff', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'auth_provider', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
        ('Phone Verifications', {'fields': ('phone_verify', 'code')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Shipping)