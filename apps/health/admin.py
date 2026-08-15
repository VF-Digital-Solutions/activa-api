from django.contrib import admin

from .models import SleepLog


@admin.register(SleepLog)
class SleepLogAdmin(admin.ModelAdmin):
    list_display = ("user", "sleep_date", "duration_hours", "quality")
    list_filter = ("quality",)
    search_fields = ("user__email", "notes")
    raw_id_fields = ("user",)
    date_hierarchy = "sleep_date"
