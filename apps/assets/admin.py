from django.contrib import admin
from .models import (
    AssetCategory, Asset, AssetDocument,
    AssetUsageLog, MaintenanceRecord, MaintenanceTemplate,
)


class AssetDocumentInline(admin.TabularInline):
    model = AssetDocument
    extra = 0
    fields = ("name", "type", "file", "mime_type", "file_size")


class MaintenanceRecordInline(admin.TabularInline):
    model = MaintenanceRecord
    extra = 0
    fields = ("title", "type", "status", "scheduled_at", "completed_at", "cost", "currency")


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    search_fields = ("name", "slug")
    raw_id_fields = ("parent",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    inlines = [AssetDocumentInline, MaintenanceRecordInline]
    list_display = ("name", "household_node", "category", "status", "purchase_date", "warranty_expiry")
    list_filter = ("status", "category")
    search_fields = ("name", "brand", "model", "serial_number")
    raw_id_fields = ("household_node", "category")
    date_hierarchy = "purchase_date"


@admin.register(AssetDocument)
class AssetDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "asset", "type", "mime_type", "file_size")
    list_filter = ("type",)
    search_fields = ("name", "asset__name")
    raw_id_fields = ("asset", "uploaded_by")


@admin.register(AssetUsageLog)
class AssetUsageLogAdmin(admin.ModelAdmin):
    list_display = ("asset", "metric", "value", "unit", "recorded_at")
    search_fields = ("asset__name", "metric")
    raw_id_fields = ("asset", "recorded_by")
    date_hierarchy = "recorded_at"


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "asset", "type", "status", "scheduled_at", "cost", "currency")
    list_filter = ("type", "status")
    search_fields = ("title", "asset__name", "provider_name")
    raw_id_fields = ("asset", "performed_by")
    date_hierarchy = "scheduled_at"


@admin.register(MaintenanceTemplate)
class MaintenanceTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "suggested_interval_days")
    search_fields = ("title", "category__name")
    raw_id_fields = ("category",)
