from django.contrib import admin

from .models import TimeBlock


@admin.register(TimeBlock)
class TimeBlockAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "existential_category",
        "energy_tag",
        "status",
        "start_datetime",
        "duration_minutes",
    )
    list_filter = ("existential_category", "energy_tag", "status")
    search_fields = ("title", "user__email")
    raw_id_fields = ("user", "replaced_by")
    date_hierarchy = "start_datetime"
