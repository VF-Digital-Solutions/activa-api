from django.contrib import admin
from .models import AgendaEvent


@admin.register(AgendaEvent)
class AgendaEventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "user", "starts_at", "ends_at", "is_active")
    list_filter = ("event_type", "is_all_day", "is_active")
    search_fields = ("title", "description", "user__email")
    date_hierarchy = "starts_at"
    filter_horizontal = ("attendees",)
