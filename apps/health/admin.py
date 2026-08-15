from django.contrib import admin

from .models import ActivityLog, SleepLog


@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = ("user", "sleep_date", "duration_hours", "quality")
    list_filter = ("quality",)
    search_fields = ("user__email", "notes")
    raw_id_fields = ("user",)
    date_hierarchy = "sleep_date"


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_type", "duration_minutes", "intensity", "recorded_at")
    list_filter = ("activity_type", "intensity")
    search_fields = ("user__email", "notes")
    raw_id_fields = ("user",)
    date_hierarchy = "recorded_at"
