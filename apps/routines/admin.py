from django.contrib import admin
from .models import (
    Habit, HabitLog, HabitStreak,
    HouseholdRoutine, HouseholdRoutineOccurrence,
)


class HabitLogInline(admin.TabularInline):
    model = HabitLog
    extra = 0
    fields = ("logged_at", "status", "value", "notes")


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    inlines = [HabitLogInline]
    list_display = ("name", "user", "category", "frequency_type", "visibility", "start_date", "archived_at")
    list_filter = ("category", "frequency_type", "visibility")
    search_fields = ("name", "user__email")
    raw_id_fields = ("user", "household_node")
    date_hierarchy = "start_date"


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ("habit", "logged_at", "status", "value")
    list_filter = ("status",)
    search_fields = ("habit__name",)
    raw_id_fields = ("habit", "logged_by")
    date_hierarchy = "logged_at"


@admin.register(HabitStreak)
class HabitStreakAdmin(admin.ModelAdmin):
    list_display = ("habit", "current_streak", "longest_streak", "total_completions", "last_completed_at")
    search_fields = ("habit__name",)
    raw_id_fields = ("habit",)


class HouseholdRoutineOccurrenceInline(admin.TabularInline):
    model = HouseholdRoutineOccurrence
    extra = 0
    fields = ("assigned_to", "due_at", "status", "completed_at", "completed_by")
    raw_id_fields = ("assigned_to", "completed_by")


@admin.register(HouseholdRoutine)
class HouseholdRoutineAdmin(admin.ModelAdmin):
    inlines = [HouseholdRoutineOccurrenceInline]
    list_display = ("title", "household_node", "category", "recurrence_type", "is_rotative")
    list_filter = ("category", "recurrence_type", "is_rotative")
    search_fields = ("title", "household_node__name")
    raw_id_fields = ("household_node", "created_by", "linked_asset")


@admin.register(HouseholdRoutineOccurrence)
class HouseholdRoutineOccurrenceAdmin(admin.ModelAdmin):
    list_display = ("routine", "assigned_to", "due_at", "status", "completed_at")
    list_filter = ("status",)
    search_fields = ("routine__title", "assigned_to__email")
    raw_id_fields = ("routine", "assigned_to", "completed_by")
    date_hierarchy = "due_at"
