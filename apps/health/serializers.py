from rest_framework import serializers

from apps.health.models import (
    ActivityLog,
    Medication,
    MedicationDoseLog,
    NutritionLog,
    SleepLog,
)


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


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = [
            "id",
            "name",
            "dosage",
            "frequency",
            "reminder_times",
            "start_date",
            "end_date",
            "is_active",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class MedicationDoseLogSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source="medication.name", read_only=True)

    class Meta:
        model = MedicationDoseLog
        fields = [
            "id",
            "medication",
            "medication_name",
            "status",
            "notes",
            "taken_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_medication(self, value):
        request = self.context["request"]
        if value.user_id != request.user.id:
            raise serializers.ValidationError("Medicación inválida.")
        return value


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
