from django.contrib import admin
from .models import AlertTemplate, Alert


@admin.register(AlertTemplate)
class AlertTemplateAdmin(admin.ModelAdmin):
    list_display = ("type", "title_template", "default_channels")
    search_fields = ("type", "title_template")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("type", "target_user", "title", "status", "scheduled_at", "sent_at", "retry_count")
    list_filter = ("type", "status")
    search_fields = ("title", "target_user__email", "body")
    raw_id_fields = ("target_user", "source_content_type")
    readonly_fields = ("sent_at", "read_at")
    date_hierarchy = "scheduled_at"
