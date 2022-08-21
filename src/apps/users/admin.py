from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (_("Extra info"), {"fields": ("updated",)}),
    )
    readonly_fields = ("updated",)
