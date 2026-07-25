from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.identity.models import User


class Assessment(TimeStampedModel):
    """Plantilla versionada de un cuestionario (auditoría de 7 áreas o escala de salud existencial)."""

    class Type(models.TextChoices):
        AUDIT_7_AREAS = "AUDIT_7_AREAS", "Auditoría de las siete áreas"
        HEALTH_SCALE_10 = "HEALTH_SCALE_10", "Escala de salud existencial de 10 indicadores"

    type = models.CharField(max_length=20, choices=Type.choices)
    version = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "assessment_assessment"
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        unique_together = ("type", "version")
        ordering = ["type", "-version"]

    def __str__(self):
        return f"{self.get_type_display()} v{self.version}"


class Question(TimeStampedModel):
    """Pregunta individual de una evaluación, asociada a una dimensión de capital existencial."""

    class CapitalDimension(models.TextChoices):
        PHYSICAL = "PHYSICAL", "Físico"
        EMOTIONAL = "EMOTIONAL", "Emocional"
        RELATIONAL = "RELATIONAL", "Relacional"
        COGNITIVE = "COGNITIVE", "Cognitivo"
        MORAL = "MORAL", "Moral"
        TRANSCENDENTAL = "TRANSCENDENTAL", "Trascendental"
        STRENGTHS = "STRENGTHS", "Fortalezas"

    class ScaleType(models.TextChoices):
        SCALE_1_10 = "SCALE_1_10", "Escala 1-10"

    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    order = models.PositiveIntegerField()
    capital_dimension = models.CharField(
        max_length=20, choices=CapitalDimension.choices
    )
    scale_type = models.CharField(
        max_length=20, choices=ScaleType.choices, default=ScaleType.SCALE_1_10
    )

    class Meta:
        db_table = "assessment_question"
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ["assessment", "order"]
        unique_together = ("assessment", "order")

    def __str__(self):
        return f"{self.assessment} — #{self.order}"


class AssessmentAttempt(TimeStampedModel):
    """Una sesión de evaluación de un usuario: agrupa las respuestas de una sola vez que se responde el cuestionario."""

    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "En progreso"
        COMPLETED = "COMPLETED", "Completada"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assessment_attempts"
    )
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="attempts"
    )
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.IN_PROGRESS
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "assessment_attempt"
        verbose_name = "Intento de evaluación"
        verbose_name_plural = "Intentos de evaluación"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} — {self.assessment} ({self.status})"


class AssessmentResponse(TimeStampedModel):
    """Respuesta de un usuario a una pregunta, con puntaje numérico y marca de tiempo."""

    attempt = models.ForeignKey(
        AssessmentAttempt, on_delete=models.CASCADE, related_name="responses"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assessment_responses"
    )
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="responses"
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        db_table = "assessment_response"
        verbose_name = "Respuesta de evaluación"
        verbose_name_plural = "Respuestas de evaluación"
        ordering = ["-created_at"]
        unique_together = ("attempt", "question")

    def __str__(self):
        return f"{self.user} — {self.question} = {self.score}"


class AssessmentSnapshot(TimeStampedModel):
    """Fotografía fechada de los puntajes por dimensión al completar un intento de evaluación."""

    attempt = models.OneToOneField(
        AssessmentAttempt, on_delete=models.CASCADE, related_name="snapshot"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assessment_snapshots"
    )
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="snapshots"
    )
    snapshot_date = models.DateField(auto_now_add=True)
    scores_by_dimension = models.JSONField(default=dict)

    class Meta:
        db_table = "assessment_snapshot"
        verbose_name = "Snapshot de evaluación"
        verbose_name_plural = "Snapshots de evaluación"
        ordering = ["-snapshot_date"]

    def __str__(self):
        return f"{self.user} — {self.assessment} @ {self.snapshot_date}"
