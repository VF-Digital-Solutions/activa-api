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


class Medication(TimeStampedModel):
    """Un medicamento con su esquema de dosis y horarios de recordatorio."""

    class Frequency(models.TextChoices):
        ONCE_DAILY = "ONCE_DAILY", "Una vez al día"
        TWICE_DAILY = "TWICE_DAILY", "Dos veces al día"
        THREE_TIMES_DAILY = "THREE_TIMES_DAILY", "Tres veces al día"
        WEEKLY = "WEEKLY", "Semanal"
        AS_NEEDED = "AS_NEEDED", "Según necesidad"
        OTHER = "OTHER", "Otra"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="medications"
    )
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    reminder_times = models.JSONField(
        default=list,
        blank=True,
        help_text="Horarios de recordatorio, formato HH:MM (ej. ['08:00', '20:00']).",
    )
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "health_medication"
        verbose_name = "Medicación"
        verbose_name_plural = "Medicaciones"
        ordering = ["-is_active", "name"]

    def __str__(self):
        return f"{self.user} — {self.name} ({self.dosage})"


class MedicationDoseLog(TimeStampedModel):
    """Registro de que una dosis fue tomada u omitida."""

    class Status(models.TextChoices):
        TAKEN = "TAKEN", "Tomada"
        SKIPPED = "SKIPPED", "Omitida"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="medication_dose_logs"
    )
    medication = models.ForeignKey(
        Medication, on_delete=models.CASCADE, related_name="dose_logs"
    )
    taken_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "health_medication_dose_log"
        verbose_name = "Registro de dosis"
        verbose_name_plural = "Registros de dosis"
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.medication.name} — {self.get_status_display()} ({self.taken_at.date()})"


class BiometricLog(TimeStampedModel):
    """Registro de un indicador biométrico.

    value siempre se usa; secondary_value solo aplica a BLOOD_PRESSURE
    (sistólica en value, diastólica en secondary_value). Múltiples
    entradas por día, cada una con su propio timestamp.
    """

    class IndicatorType(models.TextChoices):
        WEIGHT = "WEIGHT", "Peso (kg)"
        BLOOD_PRESSURE = "BLOOD_PRESSURE", "Presión arterial (mmHg)"
        HEART_RATE = "HEART_RATE", "Frecuencia cardíaca (lpm)"
        BLOOD_GLUCOSE = "BLOOD_GLUCOSE", "Glucosa en sangre (mg/dL)"
        BODY_TEMPERATURE = "BODY_TEMPERATURE", "Temperatura corporal (°C)"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="biometric_logs"
    )
    recorded_at = models.DateTimeField(default=timezone.now)
    indicator_type = models.CharField(max_length=20, choices=IndicatorType.choices)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    secondary_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "health_biometric_log"
        verbose_name = "Indicador biométrico"
        verbose_name_plural = "Indicadores biométricos"
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.user} — {self.get_indicator_type_display()} ({self.value})"
