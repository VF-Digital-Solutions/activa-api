from django.contrib import admin
from .models import HouseholdNode, HouseholdMembership, HouseholdInvitation


class HouseholdMembershipInline(admin.TabularInline):
    model = HouseholdMembership
    extra = 0
    raw_id_fields = ("user", "invited_by")
    fields = ("user", "role", "nickname", "joined_at", "left_at", "invited_by")
    readonly_fields = ("joined_at",)


@admin.register(HouseholdNode)
class HouseholdNodeAdmin(admin.ModelAdmin):
    inlines = [HouseholdMembershipInline]
    list_display = ("name", "type", "parent", "is_active")
    list_filter = ("type",)
    search_fields = ("name",)
    raw_id_fields = ("parent",)


@admin.register(HouseholdMembership)
class HouseholdMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "node", "role", "joined_at", "left_at")
    list_filter = ("role",)
    search_fields = ("user__email", "node__name")
    raw_id_fields = ("user", "node", "invited_by")
    date_hierarchy = "joined_at"


@admin.register(HouseholdInvitation)
class HouseholdInvitationAdmin(admin.ModelAdmin):
    list_display = ("invited_email", "node", "role", "status", "expires_at")
    list_filter = ("status", "role")
    search_fields = ("invited_email", "node__name")
    raw_id_fields = ("node", "invited_by")
    readonly_fields = ("token",)
