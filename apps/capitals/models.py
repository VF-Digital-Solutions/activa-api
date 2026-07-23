from django.core.validators import MaxValueValidator, MinValueValidator
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


class EmotionalLog(CapitalEntry):
    """Registro de una emoción vivida, con intensidad y nota de contexto opcional.

    Permite múltiples entradas por día, cada una con su propio timestamp
    (recorded_at, heredado de CapitalEntry).
    """

    class Emotion(models.TextChoices):
        JOY = "JOY", "Alegría"
        GRATITUDE = "GRATITUDE", "Gratitud"
        CALM = "CALM", "Calma"
        LOVE = "LOVE", "Amor"
        PRIDE = "PRIDE", "Orgullo"
        SADNESS = "SADNESS", "Tristeza"
        ANGER = "ANGER", "Ira"
        FEAR = "FEAR", "Miedo"
        ANXIETY = "ANXIETY", "Ansiedad"
        FRUSTRATION = "FRUSTRATION", "Frustración"
        LONELINESS = "LONELINESS", "Soledad"
        SHAME = "SHAME", "Vergüenza"

    emotion = models.CharField(max_length=20, choices=Emotion.choices)
    intensity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    context_note = models.TextField(blank=True)

    class Meta:
        db_table = "capitals_emotional_log"
        verbose_name = "Registro emocional"
        verbose_name_plural = "Registros emocionales"
        ordering = ["-recorded_at"]

    def save(self, *args, **kwargs):
        self.capital_type = self.CapitalType.EMOTIONAL
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} — {self.get_emotion_display()} ({self.intensity})"
