from django.db import models
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.identity.models import User


class CapitalEntry(TimeStampedModel):
    """Base abstracta para registros de datos contra uno de los siete capitales existenciales.

    Diseñada para las siete dimensiones (físico, emocional, relacional,
    cognitivo, moral, trascendental, fortalezas); en el MVP solo el capital
    emocional tiene un modelo concreto (ver EmotionalLog).
    """

    class CapitalType(models.TextChoices):
        PHYSICAL = "PHYSICAL", "Físico"
        EMOTIONAL = "EMOTIONAL", "Emocional"
        RELATIONAL = "RELATIONAL", "Relacional"
        COGNITIVE = "COGNITIVE", "Cognitivo"
        MORAL = "MORAL", "Moral"
        TRANSCENDENTAL = "TRANSCENDENTAL", "Trascendental"
        STRENGTHS = "STRENGTHS", "Fortalezas"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_set"
    )
    recorded_at = models.DateTimeField(default=timezone.now)
    capital_type = models.CharField(max_length=20, choices=CapitalType.choices)

    class Meta:
        abstract = True
        ordering = ["-recorded_at"]
