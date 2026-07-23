from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import TimeStampedModel
from apps.identity.models import User


class TimeBlock(TimeStampedModel):
    """Bloque de tiempo vital: unidad principal de la agenda existencial de Activa."""

    class ExistentialCategory(models.TextChoices):
        OBLIGATIONS = "OBLIGATIONS", "Obligaciones"
        INNER_NOURISHMENT = "INNER_NOURISHMENT", "Nutrición interior"
        BONDS = "BONDS", "Vínculos"
        TRANSCENDENCE = "TRANSCENDENCE", "Trascendencia"

    class EnergyTag(models.TextChoices):
        ENERGIZES = "ENERGIZES", "Energiza"
        NEUTRAL = "NEUTRAL", "Neutro"
        DRAINS = "DRAINS", "Drena"

    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planificado"
        FULFILLED = "FULFILLED", "Cumplido"
        OMITTED = "OMITTED", "Omitido"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="time_blocks"
    )
    title = models.CharField(max_length=150)
    existential_category = models.CharField(
        max_length=20, choices=ExistentialCategory.choices
    )
    energy_tag = models.CharField(max_length=10, choices=EnergyTag.choices)
    duration_minutes = models.PositiveIntegerField()
    start_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PLANNED
    )

    # GenericForeignKey opcional hacia el objeto de origen (p.ej. un hábito
    # o evento externo que dio pie a este bloque).
    source_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    source_object_id = models.UUIDField(null=True, blank=True)
    source = GenericForeignKey("source_content_type", "source_object_id")

    # Auto-referencia opcional: si el bloque fue omitido y reemplazado por
    # otro (reasignación de tiempo, no fallo de cumplimiento).
    replaced_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replaces",
    )

    class Meta:
        db_table = "agenda_time_block"
        verbose_name = "Bloque de tiempo"
        verbose_name_plural = "Bloques de tiempo"
        ordering = ["-start_datetime", "-created_at"]

    def __str__(self):
        return f"{self.user} — {self.title} ({self.status})"
