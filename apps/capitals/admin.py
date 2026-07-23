from django.contrib import admin

from .models import EmotionalLog, JournalEntry


@admin.register(EmotionalLog)
class EmotionalLogAdmin(admin.ModelAdmin):
    list_display = ("user", "emotion", "intensity", "recorded_at")
    list_filter = ("emotion",)
    search_fields = ("user__email", "context_note")
    raw_id_fields = ("user",)
    date_hierarchy = "recorded_at"


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "recorded_at")
    search_fields = ("user__email",)
    raw_id_fields = ("user",)
    date_hierarchy = "recorded_at"
