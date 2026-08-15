from rest_framework import serializers

from apps.health.models import ActivityLog, NutritionLog, SleepLog


class SleepLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepLog
        fields = [
            "id",
            "sleep_date",
            "bedtime",
            "wake_time",
            "duration_hours",
            "quality",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class NutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionLog
        fields = [
            "id",
            "meal_type",
            "description",
            "calories",
            "recorded_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "activity_type",
            "duration_minutes",
            "intensity",
            "calories_burned",
            "notes",
            "recorded_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
