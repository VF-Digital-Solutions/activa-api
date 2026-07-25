"""Generadores de EmotionalLog / JournalEntry para el seed de datos de demo.

A diferencia de un seed puramente aleatorio, estos generadores reciben un
`mood_bias` derivado de la agenda real del día (ver `derive_mood_bias`), para
que las emociones y el diario queden correlacionados con cómo fue ese día en
vez de ser ruido independiente.
"""

from datetime import datetime, time

from django.utils import timezone

from apps.capitals.models import EmotionalLog, JournalEntry
from apps.core.demo_data.config import (
    EMOTION_POOL_NEGATIVE,
    EMOTION_POOL_POSITIVE,
    EMOTIONAL_LOG_NOTES_NEGATIVE,
    EMOTIONAL_LOG_NOTES_POSITIVE,
    JOURNAL_TEMPLATES_NEGATIVE,
    JOURNAL_TEMPLATES_POSITIVE,
)

_TZ = timezone.get_current_timezone()

_CATEGORY_LABELS_ES = {
    "OBLIGATIONS": "Las obligaciones",
    "INNER_NOURISHMENT": "El cuidado personal",
    "BONDS": "Los vínculos",
    "TRANSCENDENCE": "El tiempo de trascendencia",
}


def _aware(date, hour, minute=0):
    return timezone.make_aware(datetime.combine(date, time(hour, minute)), _TZ)


def derive_mood_bias(distribution, coherence):
    """Sesgo de ánimo del día en [-1, 1], a partir de la agenda real.

    Combina la proporción de minutos ENERGIZES vs DRAINS (mitad del peso) y
    el índice de coherencia intención-vs-ejecución (la otra mitad). Un día
    con más DRAINS que ENERGIZES y baja coherencia da un bias negativo; lo
    inverso da un bias positivo.
    """
    assigned = max(distribution["assigned_minutes"], 1)
    drains_ratio = distribution["by_energy_tag"].get("DRAINS", 0) / assigned
    energizes_ratio = distribution["by_energy_tag"].get("ENERGIZES", 0) / assigned

    coherence_index = coherence["coherence_index"]
    coherence_component = (coherence_index if coherence_index is not None else 0.5) * 2 - 1

    mood_bias = 0.5 * (energizes_ratio - drains_ratio) + 0.5 * coherence_component
    return round(min(1.0, max(-1.0, mood_bias)), 2)


def _positive_probability(mood_bias):
    return min(0.9, max(0.1, 0.5 + mood_bias / 2))


def _intensity_for(is_positive, mood_bias, rng):
    if is_positive:
        low, high = (6, 9) if mood_bias >= 0 else (4, 7)
    else:
        low, high = (6, 9) if mood_bias <= 0 else (3, 6)
    return rng.randint(low, high)


def generate_emotional_logs_for_day(user, date, rng, mood_bias):
    """Crea 1-3 EmotionalLog para el día, sesgados por `mood_bias`."""
    positive_probability = _positive_probability(mood_bias)

    logs = []
    for _ in range(rng.randint(1, 3)):
        is_positive = rng.random() < positive_probability
        emotion = rng.choice(EMOTION_POOL_POSITIVE if is_positive else EMOTION_POOL_NEGATIVE)
        note = rng.choice(
            EMOTIONAL_LOG_NOTES_POSITIVE if is_positive else EMOTIONAL_LOG_NOTES_NEGATIVE
        )
        logs.append(
            EmotionalLog(
                user=user,
                recorded_at=_aware(date, rng.randint(8, 22), rng.choice([0, 20, 40])),
                emotion=emotion,
                intensity=_intensity_for(is_positive, mood_bias, rng),
                context_note=note,
            )
        )
    return EmotionalLog.objects.bulk_create(logs)


def _top_drain_category(distribution):
    by_category = {
        category: minutes
        for category, minutes in distribution["by_category"].items()
        if category != "UNASSIGNED" and minutes > 0
    }
    if not by_category:
        return "El día en general"
    top = max(by_category, key=by_category.get)
    return _CATEGORY_LABELS_ES.get(top, top)


def _render(template, distribution, coherence):
    return template.format(
        top_drain_category=_top_drain_category(distribution),
        coherence_index=coherence["coherence_index"],
    )


def generate_journal_entry_for_day(user, date, rng, mood_bias, distribution, coherence):
    """Crea la entrada de diario del día, usando las plantillas positivas o
    negativas según `mood_bias`, interpoladas con datos reales de la agenda
    de ese día (categoría más drenante, índice de coherencia)."""
    templates = JOURNAL_TEMPLATES_POSITIVE if mood_bias >= 0 else JOURNAL_TEMPLATES_NEGATIVE

    fields = {}
    for field_name, options in templates.items():
        fields[field_name] = _render(rng.choice(options), distribution, coherence)

    return JournalEntry.objects.create(
        user=user,
        recorded_at=_aware(date, 22, 30),
        **fields,
    )
