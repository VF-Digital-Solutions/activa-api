from rest_framework import serializers
from apps.reservations.models import (
    ReservationCategory,
    Reservation,
    ReservationReminder,
    ReservationDocument,
)


class ReservationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationCategory
        fields = ["id", "name", "slug", "icon", "color"]
        read_only_fields = ["id"]


class ReservationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationReminder
        fields = ["id", "reservation", "remind_at", "channels", "sent"]
        read_only_fields = ["id", "sent"]


class ReservationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationDocument
        fields = ["id", "reservation", "name", "type", "file_url"]
        read_only_fields = ["id"]


class ReservationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    reminders = ReservationReminderSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "household_node",
            "category",
            "category_name",
            "title",
            "description",
            "type",
            "status",
            "starts_at",
            "ends_at",
            "is_all_day",
            "timezone",
            "location_name",
            "location_address",
            "provider_name",
            "provider_contact",
            "meeting_url",
            "confirmation_code",
            "cost",
            "currency",
            "notes",
            "linked_asset",
            "attendees",
            "reminders",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
