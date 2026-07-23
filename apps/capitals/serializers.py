from rest_framework import serializers

from apps.capitals.models import EmotionalLog


class EmotionalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionalLog
        fields = [
            "id",
            "emotion",
            "intensity",
            "context_note",
            "recorded_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
