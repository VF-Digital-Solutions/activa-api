from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.identity.models import User
from apps.households.models import HouseholdNode
from apps.assets.models import Asset


class ReservationCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "reservations_category"
        verbose_name = "Categoría de reserva"
        verbose_name_plural = "Categorías de reservas"

    def __str__(self):
        return self.name


class Reservation(SoftDeleteModel):

    class Type(models.TextChoices):
        APPOINTMENT = "APPOINTMENT", "Cita"
        ACTIVITY = "ACTIVITY", "Actividad"
        SERVICE = "SERVICE", "Servicio"
        EVENT = "EVENT", "Evento"
        OTHER = "OTHER", "Otro"

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Programado"
        CONFIRMED = "CONFIRMED", "Confirmado"
        COMPLETED = "COMPLETED", "Completado"
        CANCELLED = "CANCELLED", "Cancelado"
        NO_SHOW = "NO_SHOW", "No asistió"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    household_node = models.ForeignKey(
        HouseholdNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations",
    )
    category = models.ForeignKey(
        ReservationCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations",
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=15, choices=Type.choices, default=Type.OTHER)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.SCHEDULED
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default="UTC")
    location_name = models.CharField(max_length=150, blank=True)
    location_address = models.JSONField(default=dict, blank=True)
    provider_name = models.CharField(max_length=150, blank=True)
    provider_contact = models.CharField(max_length=150, blank=True)
    meeting_url = models.URLField(blank=True, null=True)
    confirmation_code = models.CharField(max_length=100, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)
    linked_asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservations",
    )
    attendees = models.ManyToManyField(
        User, blank=True, related_name="attending_reservations"
    )

    class Meta:
        db_table = "reservations_reservation"
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.title} — {self.starts_at}"


class ReservationReminder(TimeStampedModel):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="reminders"
    )
    remind_at = models.DateTimeField()
    channels = models.JSONField(default=list)
    sent = models.BooleanField(default=False)

    class Meta:
        db_table = "reservations_reminder"
        verbose_name = "Recordatorio de reserva"
        verbose_name_plural = "Recordatorios de reservas"

    def __str__(self):
        return f"{self.reservation.title} — {self.remind_at}"


class ReservationDocument(TimeStampedModel):

    class DocType(models.TextChoices):
        CONFIRMATION = "CONFIRMATION", "Confirmación"
        RESULT = "RESULT", "Resultado"
        RECEIPT = "RECEIPT", "Recibo"
        OTHER = "OTHER", "Otro"

    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=150)
    type = models.CharField(
        max_length=15, choices=DocType.choices, default=DocType.OTHER
    )
    file_url = models.URLField()

    class Meta:
        db_table = "reservations_document"
        verbose_name = "Documento de reserva"
        verbose_name_plural = "Documentos de reservas"

    def __str__(self):
        return f"{self.name} — {self.reservation.title}"
