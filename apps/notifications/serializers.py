from rest_framework import serializers
from apps.notifications.models import Alert, AlertTemplate


class AlertTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertTemplate
        fields = [
            "id",
            "type",
            "title_template",
            "body_template",
            "default_channels",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            "id",
            "target_user",
            "type",
            "title",
            "body",
            "action_url",
            "metadata",
            "channels",
            "scheduled_at",
            "sent_at",
            "read_at",
            "status",
            "retry_count",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "target_user",
            "sent_at",
            "read_at",
            "status",
            "retry_count",
            "created_at",
        ]
