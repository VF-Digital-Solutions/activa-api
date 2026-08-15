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


class ActivityLog(TimeStampedModel):
    """Registro de una sesión de actividad física.

    Múltiples entradas por día, cada una con su propio timestamp
    (recorded_at), a diferencia de SleepLog que es una por noche.
    """

    class ActivityType(models.TextChoices):
        WALK = "WALK", "Caminata"
        RUN = "RUN", "Running"
        CYCLING = "CYCLING", "Ciclismo"
        SWIMMING = "SWIMMING", "Natación"
        STRENGTH = "STRENGTH", "Fuerza"
        YOGA = "YOGA", "Yoga"
        SPORTS = "SPORTS", "Deporte"
        OTHER = "OTHER", "Otra"

    class Intensity(models.TextChoices):
        LOW = "LOW", "Baja"
        MODERATE = "MODERATE", "Moderada"
        HIGH = "HIGH", "Alta"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_logs"
    )
    recorded_at = models.DateTimeField(default=timezone.now)
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1440)]
    )
    intensity = models.CharField(max_length=10, choices=Intensity.choices)
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "health_activity_log"
        verbose_name = "Registro de actividad física"
        verbose_name_plural = "Registros de actividad física"
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.user} — {self.get_activity_type_display()} ({self.duration_minutes}min)"


class NutritionLog(TimeStampedModel):
    """Registro de una comida. Múltiples entradas por día, una por comida."""

    class MealType(models.TextChoices):
        BREAKFAST = "BREAKFAST", "Desayuno"
        LUNCH = "LUNCH", "Almuerzo"
        DINNER = "DINNER", "Cena"
        SNACK = "SNACK", "Colación"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="nutrition_logs"
    )
    recorded_at = models.DateTimeField(default=timezone.now)
    meal_type = models.CharField(max_length=10, choices=MealType.choices)
    description = models.TextField()
    calories = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "health_nutrition_log"
        verbose_name = "Registro de nutrición"
        verbose_name_plural = "Registros de nutrición"
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.user} — {self.get_meal_type_display()} ({self.recorded_at.date()})"
