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


class AssessmentResponse(TimeStampedModel):
    """Respuesta de un usuario a una pregunta, con puntaje numérico y marca de tiempo."""

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

    def __str__(self):
        return f"{self.user} — {self.question} = {self.score}"
