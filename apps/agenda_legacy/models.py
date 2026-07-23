import uuid
from django.db import models
from apps.core.models import TimeStampedModel
from apps.identity.models import User
from apps.households.models import HouseholdNode


class AgendaEvent(TimeStampedModel):

    class EventType(models.TextChoices):
        PERSONAL = "PERSONAL", "Personal"
        HOUSEHOLD = "HOUSEHOLD", "Del hogar"
        REMINDER = "REMINDER", "Recordatorio"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agenda_events")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    event_type = models.CharField(
        max_length=10, choices=EventType.choices, default=EventType.PERSONAL
    )

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)

    # Solo relevante cuando event_type=HOUSEHOLD
    household_node = models.ForeignKey(
        HouseholdNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agenda_events",
    )
    attendees = models.ManyToManyField(
        User, related_name="attending_agenda_events", blank=True
    )

    # Solo relevante cuando event_type=REMINDER
    remind_at = models.DateTimeField(null=True, blank=True)
    channels = models.JSONField(default=list, blank=True)
    reminder_sent = models.BooleanField(default=False)

    color = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "agenda_event"
        verbose_name = "Evento de agenda"
        verbose_name_plural = "Eventos de agenda"
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.title} ({self.event_type}) — {self.starts_at:%Y-%m-%d %H:%M}"
