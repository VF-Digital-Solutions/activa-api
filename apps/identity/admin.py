from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserDevice


class UserDeviceInline(admin.TabularInline):
    model = UserDevice
    extra = 0
    readonly_fields = ("last_seen_at",)
    fields = ("platform", "device_token", "is_active", "last_seen_at")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserDeviceInline]
    list_display = ("email", "username", "first_name", "last_name", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superuser", "preferred_language")
    search_fields = ("email", "username", "first_name", "last_name", "phone_number")
    ordering = ("-date_joined",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Perfil", {"fields": ("phone_number", "avatar_url", "preferred_language", "timezone", "notification_preferences")}),
    )


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "is_active", "last_seen_at")
    list_filter = ("platform", "is_active")
    search_fields = ("user__email", "device_token")
    raw_id_fields = ("user",)
    readonly_fields = ("last_seen_at",)
