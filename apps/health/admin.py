from django.contrib import admin

from .models import ActivityLog, Medication, MedicationDoseLog, NutritionLog, SleepLog


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


@admin.register(NutritionLog)
class NutritionLogAdmin(admin.ModelAdmin):
    list_display = ("user", "meal_type", "calories", "recorded_at")
    list_filter = ("meal_type",)
    search_fields = ("user__email", "description")
    raw_id_fields = ("user",)
    date_hierarchy = "recorded_at"


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "dosage", "frequency", "is_active")
    list_filter = ("frequency", "is_active")
    search_fields = ("user__email", "name")
    raw_id_fields = ("user",)


@admin.register(MedicationDoseLog)
class MedicationDoseLogAdmin(admin.ModelAdmin):
    list_display = ("user", "medication", "status", "taken_at")
    list_filter = ("status",)
    search_fields = ("user__email", "medication__name")
    raw_id_fields = ("user", "medication")
    date_hierarchy = "taken_at"
