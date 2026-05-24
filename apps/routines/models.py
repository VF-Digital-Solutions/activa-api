from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.identity.models import User
from apps.households.models import HouseholdNode
from apps.assets.models import Asset


class Habit(SoftDeleteModel):

    class Category(models.TextChoices):
        HEALTH = "HEALTH", "Salud"
        FITNESS = "FITNESS", "Ejercicio"
        LEARNING = "LEARNING", "Aprendizaje"
        HOME = "HOME", "Hogar"
        FINANCE = "FINANCE", "Finanzas"
        CUSTOM = "CUSTOM", "Personalizado"

    class FrequencyType(models.TextChoices):
        DAILY = "DAILY", "Diario"
        WEEKLY = "WEEKLY", "Semanal"
        CUSTOM = "CUSTOM", "Personalizado"

    class Visibility(models.TextChoices):
        PRIVATE = "PRIVATE", "Privado"
        HOUSEHOLD = "HOUSEHOLD", "Hogar"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    household_node = models.ForeignKey(
        HouseholdNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="habits",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=10, blank=True)
    category = models.CharField(
        max_length=15, choices=Category.choices, default=Category.CUSTOM
    )
    visibility = models.CharField(
        max_length=15, choices=Visibility.choices, default=Visibility.PRIVATE
    )
    frequency_type = models.CharField(
        max_length=10, choices=FrequencyType.choices, default=FrequencyType.DAILY
    )
    frequency_config = models.JSONField(default=dict, blank=True)
    target_value = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    target_unit = models.CharField(max_length=30, blank=True)
    reminder_time = models.TimeField(null=True, blank=True)
    start_date = models.DateField()
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "routines_habit"
        verbose_name = "Hábito"
        verbose_name_plural = "Hábitos"

    def __str__(self):
        return f"{self.name} — {self.user.email}"


class HabitLog(TimeStampedModel):

    class Status(models.TextChoices):
        COMPLETED = "COMPLETED", "Completado"
        SKIPPED = "SKIPPED", "Omitido"
        PARTIAL = "PARTIAL", "Parcial"

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    logged_at = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)
    value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "routines_habit_log"
        verbose_name = "Registro de hábito"
        verbose_name_plural = "Registros de hábitos"
        unique_together = [["habit", "logged_at"]]
        ordering = ["-logged_at"]

    def __str__(self):
        return f"{self.habit.name} — {self.logged_at} ({self.status})"


class HabitStreak(TimeStampedModel):
    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, related_name="streak")
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_completed_at = models.DateField(null=True, blank=True)
    total_completions = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "routines_habit_streak"
        verbose_name = "Racha de hábito"
        verbose_name_plural = "Rachas de hábitos"

    def __str__(self):
        return f"{self.habit.name} — racha: {self.current_streak}"


class HouseholdRoutine(SoftDeleteModel):

    class Category(models.TextChoices):
        CLEANING = "CLEANING", "Limpieza"
        MAINTENANCE = "MAINTENANCE", "Mantenimiento"
        SHOPPING = "SHOPPING", "Compras"
        COOKING = "COOKING", "Cocina"
        CUSTOM = "CUSTOM", "Personalizado"

    class RecurrenceType(models.TextChoices):
        ONCE = "ONCE", "Una vez"
        DAILY = "DAILY", "Diario"
        WEEKLY = "WEEKLY", "Semanal"
        MONTHLY = "MONTHLY", "Mensual"
        CUSTOM = "CUSTOM", "Personalizado"

    household_node = models.ForeignKey(
        HouseholdNode, on_delete=models.CASCADE, related_name="routines"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_routines"
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=15, choices=Category.choices, default=Category.CUSTOM
    )
    recurrence_type = models.CharField(
        max_length=10, choices=RecurrenceType.choices, default=RecurrenceType.WEEKLY
    )
    recurrence_config = models.JSONField(default=dict, blank=True)
    estimated_duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    is_rotative = models.BooleanField(default=False)
    assignees = models.ManyToManyField(
        User, blank=True, related_name="assigned_routines"
    )
    linked_asset = models.ForeignKey(
        Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name="routines"
    )

    class Meta:
        db_table = "routines_household_routine"
        verbose_name = "Rutina del hogar"
        verbose_name_plural = "Rutinas del hogar"

    def __str__(self):
        return f"{self.title} — {self.household_node.name}"


class HouseholdRoutineOccurrence(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        IN_PROGRESS = "IN_PROGRESS", "En progreso"
        COMPLETED = "COMPLETED", "Completado"
        SKIPPED = "SKIPPED", "Omitido"

    routine = models.ForeignKey(
        HouseholdRoutine, on_delete=models.CASCADE, related_name="occurrences"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="routine_occurrences"
    )
    due_at = models.DateTimeField()
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.PENDING
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_occurrences",
    )
    notes = models.TextField(blank=True)
    proof_image_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "routines_occurrence"
        verbose_name = "Ocurrencia de rutina"
        verbose_name_plural = "Ocurrencias de rutinas"
        ordering = ["due_at"]

    def __str__(self):
        return f"{self.routine.title} — {self.due_at} ({self.status})"
