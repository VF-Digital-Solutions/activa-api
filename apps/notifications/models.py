from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel
from apps.identity.models import User
from apps.households.models import HouseholdNode


class AlertTemplate(TimeStampedModel):

    class Type(models.TextChoices):
        MAINTENANCE = "MAINTENANCE", "Mantenimiento"
        HABIT = "HABIT", "Hábito"
        ROUTINE = "ROUTINE", "Rutina"
        RESERVATION = "RESERVATION", "Reserva"
        BENEFIT = "BENEFIT", "Beneficio"
        FINANCE_BUDGET = "FINANCE_BUDGET", "Presupuesto"
        FINANCE_RECURRING = "FINANCE_RECURRING", "Gasto recurrente"
        LOYALTY_EXPIRY = "LOYALTY_EXPIRY", "Puntos por vencer"
        CUSTOM = "CUSTOM", "Personalizado"

    type = models.CharField(max_length=20, choices=Type.choices, unique=True)
    title_template = models.CharField(max_length=200)
    body_template = models.TextField()
    default_channels = models.JSONField(default=list)

    class Meta:
        db_table = "notifications_alert_template"
        verbose_name = "Plantilla de alerta"
        verbose_name_plural = "Plantillas de alertas"

    def __str__(self):
        return f"{self.type} — {self.title_template}"


class Alert(TimeStampedModel):

    class Type(models.TextChoices):
        MAINTENANCE = "MAINTENANCE", "Mantenimiento"
        HABIT = "HABIT", "Hábito"
        ROUTINE = "ROUTINE", "Rutina"
        RESERVATION = "RESERVATION", "Reserva"
        BENEFIT = "BENEFIT", "Beneficio"
        FINANCE_BUDGET = "FINANCE_BUDGET", "Presupuesto"
        FINANCE_RECURRING = "FINANCE_RECURRING", "Gasto recurrente"
        LOYALTY_EXPIRY = "LOYALTY_EXPIRY", "Puntos por vencer"
        CUSTOM = "CUSTOM", "Personalizado"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        SENT = "SENT", "Enviado"
        FAILED = "FAILED", "Fallido"
        READ = "READ", "Leído"
        CANCELLED = "CANCELLED", "Cancelado"

    target_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="alerts"
    )
    household_node = models.ForeignKey(
        HouseholdNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )

    # GenericForeignKey para desacoplar del tipo de objeto origen
    source_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    source_object_id = models.UUIDField(null=True, blank=True)
    source = GenericForeignKey("source_content_type", "source_object_id")

    type = models.CharField(max_length=20, choices=Type.choices)
    title = models.CharField(max_length=200)
    body = models.TextField()
    action_url = models.CharField(max_length=200, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    channels = models.JSONField(default=list)
    scheduled_at = models.DateTimeField()
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    retry_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "notifications_alert"
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.type} → {self.target_user.email} ({self.status})"
