from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.identity.models import User
from apps.households.models import HouseholdNode


class AssetCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    attribute_schema = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "assets_category"
        verbose_name = "Categoría de activo"
        verbose_name_plural = "Categorías de activos"

    def __str__(self):
        return self.name


class Asset(SoftDeleteModel):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activo"
        IN_REPAIR = "IN_REPAIR", "En reparación"
        INACTIVE = "INACTIVE", "Inactivo"
        DISPOSED = "DISPOSED", "Dado de baja"

    household_node = models.ForeignKey(
        HouseholdNode, on_delete=models.CASCADE, related_name="assets"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        AssetCategory, on_delete=models.SET_NULL, null=True, related_name="assets"
    )
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    warranty_expiry = models.DateField(null=True, blank=True)
    location_in_home = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.ACTIVE
    )
    attributes = models.JSONField(default=dict, blank=True)
    cover_image_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "assets_asset"
        verbose_name = "Activo"
        verbose_name_plural = "Activos"

    def __str__(self):
        return f"{self.name} — {self.household_node.name}"


class AssetDocument(TimeStampedModel):

    class DocType(models.TextChoices):
        INVOICE = "INVOICE", "Factura"
        MANUAL = "MANUAL", "Manual"
        WARRANTY = "WARRANTY", "Garantía"
        PHOTO = "PHOTO", "Foto"
        OTHER = "OTHER", "Otro"

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    type = models.CharField(
        max_length=10, choices=DocType.choices, default=DocType.OTHER
    )
    file = models.FileField(upload_to="assets/documents/", blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "assets_document"
        verbose_name = "Documento de activo"
        verbose_name_plural = "Documentos de activos"

    def __str__(self):
        return f"{self.name} — {self.asset.name}"


class AssetUsageLog(TimeStampedModel):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="usage_logs"
    )
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField()
    metric = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "assets_usage_log"
        verbose_name = "Registro de uso"
        verbose_name_plural = "Registros de uso"
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.asset.name} — {self.metric}: {self.value} {self.unit}"


class MaintenanceRecord(TimeStampedModel):

    class Type(models.TextChoices):
        PREVENTIVE = "PREVENTIVE", "Preventivo"
        CORRECTIVE = "CORRECTIVE", "Correctivo"
        INSPECTION = "INSPECTION", "Inspección"
        CLEANING = "CLEANING", "Limpieza"

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Programado"
        IN_PROGRESS = "IN_PROGRESS", "En progreso"
        COMPLETED = "COMPLETED", "Completado"
        CANCELLED = "CANCELLED", "Cancelado"

    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="maintenance_records"
    )
    title = models.CharField(max_length=150)
    type = models.CharField(max_length=15, choices=Type.choices)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.SCHEDULED
    )
    scheduled_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    provider_name = models.CharField(max_length=150, blank=True)
    provider_contact = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    documents = models.ManyToManyField(AssetDocument, blank=True)

    class Meta:
        db_table = "assets_maintenance_record"
        verbose_name = "Registro de mantenimiento"
        verbose_name_plural = "Registros de mantenimiento"
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.title} — {self.asset.name}"


class MaintenanceTemplate(TimeStampedModel):
    category = models.ForeignKey(
        AssetCategory, on_delete=models.CASCADE, related_name="maintenance_templates"
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    suggested_interval_days = models.PositiveIntegerField(null=True, blank=True)
    checklist = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "assets_maintenance_template"
        verbose_name = "Plantilla de mantenimiento"
        verbose_name_plural = "Plantillas de mantenimiento"

    def __str__(self):
        return f"{self.title} — {self.category.name}"
