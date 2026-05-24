from rest_framework import serializers
from apps.routines.models import (
    Habit,
    HabitLog,
    HabitStreak,
    HouseholdRoutine,
    HouseholdRoutineOccurrence,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "household_node",
            "name",
            "description",
            "icon",
            "color",
            "category",
            "visibility",
            "frequency_type",
            "frequency_config",
            "target_value",
            "target_unit",
            "reminder_time",
            "start_date",
            "archived_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = [
            "id",
            "habit",
            "logged_at",
            "status",
            "value",
            "notes",
            "logged_by",
            "created_at",
        ]
        read_only_fields = ["id", "logged_by", "created_at"]


class HabitStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitStreak
        fields = [
            "id",
            "habit",
            "current_streak",
            "longest_streak",
            "last_completed_at",
            "total_completions",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "habit",
            "current_streak",
            "longest_streak",
            "last_completed_at",
            "total_completions",
            "updated_at",
        ]


class HouseholdRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdRoutine
        fields = [
            "id",
            "household_node",
            "created_by",
            "title",
            "description",
            "category",
            "recurrence_type",
            "recurrence_config",
            "estimated_duration_minutes",
            "is_rotative",
            "assignees",
            "linked_asset",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class HouseholdRoutineOccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdRoutineOccurrence
        fields = [
            "id",
            "routine",
            "assigned_to",
            "due_at",
            "status",
            "completed_at",
            "completed_by",
            "notes",
            "proof_image_url",
            "created_at",
        ]
        read_only_fields = ["id", "completed_at", "completed_by", "created_at"]
