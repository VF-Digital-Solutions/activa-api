from rest_framework import serializers

from apps.capitals.models import EmotionalLog, JournalEntry


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


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = [
            "id",
            "energy_gain",
            "energy_drain",
            "avoided_conversation",
            "attention_needed",
            "gratitude",
            "recorded_at",
            "created_at",
        ]
        read_only_fields = ["id", "recorded_at", "created_at"]
