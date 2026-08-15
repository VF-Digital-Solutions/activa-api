from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.identity.models import User


class SleepLog(TimeStampedModel):
    """Registro de sueño de una noche, una entrada por fecha por usuario."""

    class Quality(models.IntegerChoices):
        VERY_POOR = 1, "Muy mala"
        POOR = 2, "Mala"
        FAIR = 3, "Regular"
        GOOD = 4, "Buena"
        EXCELLENT = 5, "Excelente"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sleep_logs"
    )
    sleep_date = models.DateField(default=timezone.localdate)
    bedtime = models.DateTimeField(null=True, blank=True)
    wake_time = models.DateTimeField(null=True, blank=True)
    duration_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
    )
    quality = models.PositiveSmallIntegerField(choices=Quality.choices)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "health_sleep_log"
        verbose_name = "Registro de sueño"
        verbose_name_plural = "Registros de sueño"
        ordering = ["-sleep_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "sleep_date"], name="unique_sleep_log_per_day"
            )
        ]

    def __str__(self):
        return f"{self.user} — {self.sleep_date} ({self.get_quality_display()})"
