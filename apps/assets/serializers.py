from rest_framework import serializers
from apps.assets.models import (
    AssetCategory,
    Asset,
    AssetDocument,
    AssetUsageLog,
    MaintenanceRecord,
    MaintenanceTemplate,
)


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = ["id", "name", "slug", "icon", "parent", "attribute_schema"]
        read_only_fields = ["id"]


class AssetSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Asset
        fields = [
            "id",
            "household_node",
            "name",
            "description",
            "category",
            "category_name",
            "brand",
            "model",
            "serial_number",
            "purchase_date",
            "purchase_price",
            "warranty_expiry",
            "location_in_home",
            "status",
            "attributes",
            "cover_image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AssetDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetDocument
        fields = [
            "id",
            "asset",
            "uploaded_by",
            "name",
            "type",
            "file_url",
            "file_size",
            "mime_type",
            "created_at",
        ]
        read_only_fields = ["id", "uploaded_by", "created_at"]


class AssetUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetUsageLog
        fields = [
            "id",
            "asset",
            "recorded_by",
            "recorded_at",
            "metric",
            "value",
            "unit",
            "notes",
        ]
        read_only_fields = ["id", "recorded_by"]


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = [
            "id",
            "asset",
            "title",
            "type",
            "status",
            "scheduled_at",
            "completed_at",
            "cost",
            "currency",
            "provider_name",
            "provider_contact",
            "notes",
            "performed_by",
            "documents",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MaintenanceTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceTemplate
        fields = [
            "id",
            "category",
            "title",
            "description",
            "suggested_interval_days",
            "checklist",
        ]
        read_only_fields = ["id"]
