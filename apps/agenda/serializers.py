from rest_framework import serializers

from apps.agenda.models import TimeBlock


class TimeBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeBlock
        fields = [
            "id",
            "title",
            "existential_category",
            "energy_tag",
            "duration_minutes",
            "start_datetime",
            "status",
            "replaced_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_replaced_by(self, replaced_by):
        request = self.context.get("request")
        if replaced_by and request and replaced_by.user_id != request.user.id:
            raise serializers.ValidationError(
                "El bloque de reemplazo debe pertenecer al mismo usuario."
            )
        return replaced_by
