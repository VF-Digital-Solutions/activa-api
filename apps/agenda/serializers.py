from rest_framework import serializers
from .models import AgendaEvent


class AgendaEventSerializer(serializers.ModelSerializer):
    attendee_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    attendees_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AgendaEvent
        fields = [
            "id",
            "title",
            "description",
            "event_type",
            "starts_at",
            "ends_at",
            "is_all_day",
            "household_node",
            "attendee_ids",
            "attendees_info",
            "remind_at",
            "channels",
            "reminder_sent",
            "color",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reminder_sent", "created_at", "updated_at"]

    def get_attendees_info(self, obj):
        return [
            {"id": str(u.id), "email": u.email, "full_name": u.get_full_name()}
            for u in obj.attendees.all()
        ]


class AgendaItemSerializer(serializers.Serializer):
    """Schema normalizado para el endpoint agregador /agenda/"""

    id = serializers.UUIDField()
    source = serializers.CharField()
    source_id = serializers.UUIDField()
    type = serializers.CharField()
    title = serializers.CharField()
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField(allow_null=True)
    is_all_day = serializers.BooleanField()
    status = serializers.CharField(allow_null=True)
    color = serializers.CharField(allow_null=True)
    metadata = serializers.DictField()
