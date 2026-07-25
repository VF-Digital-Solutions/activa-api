"""Generador de evaluaciones (Attempt/Response/Snapshot) para el seed de demo."""

from collections import defaultdict
from datetime import datetime, time

from django.utils import timezone

from apps.assessment.models import (
    Assessment,
    AssessmentAttempt,
    AssessmentResponse,
    AssessmentSnapshot,
)
from apps.core.demo_data.config import (
    ASSESSMENT_SCORE_END_RANGE,
    ASSESSMENT_SCORE_JITTER,
    ASSESSMENT_SCORE_START_RANGE,
    ASSESSMENT_SNAPSHOT_INTERVAL_DAYS,
)

_TZ = timezone.get_current_timezone()


def is_assessment_day(day_index, total_days):
    """El día 0 y el último día del rango siempre se siembran (para que el
    IVI tenga datos base desde el principio y evolucione hasta el final);
    entre medio, cada `ASSESSMENT_SNAPSHOT_INTERVAL_DAYS` días."""
    if day_index == 0 or day_index == total_days - 1:
        return True
    return day_index % ASSESSMENT_SNAPSHOT_INTERVAL_DAYS == 0


def _score_for(day_index, total_days, rng):
    progress = day_index / (total_days - 1) if total_days > 1 else 1.0
    low = ASSESSMENT_SCORE_START_RANGE[0] + (
        ASSESSMENT_SCORE_END_RANGE[0] - ASSESSMENT_SCORE_START_RANGE[0]
    ) * progress
    high = ASSESSMENT_SCORE_START_RANGE[1] + (
        ASSESSMENT_SCORE_END_RANGE[1] - ASSESSMENT_SCORE_START_RANGE[1]
    ) * progress
    score = rng.uniform(low, high) + rng.uniform(
        -ASSESSMENT_SCORE_JITTER, ASSESSMENT_SCORE_JITTER
    )
    return max(1, min(10, round(score)))


def seed_assessment_snapshot(user, date, assessment_type, day_index, total_days, rng):
    """Crea un AssessmentAttempt COMPLETED con una respuesta por pregunta
    (score interpolado entre ASSESSMENT_SCORE_START_RANGE y END_RANGE según
    el progreso dentro del rango sembrado), y su AssessmentSnapshot con
    scores_by_dimension calculado igual que AssessmentCompleteView
    (promedio por capital_dimension)."""
    assessment = Assessment.objects.filter(type=assessment_type).order_by("-version").first()
    if assessment is None:
        return None

    completed_at = timezone.make_aware(datetime.combine(date, time(20, 0)), _TZ)

    attempt = AssessmentAttempt.objects.create(
        user=user,
        assessment=assessment,
        status=AssessmentAttempt.Status.COMPLETED,
        completed_at=completed_at,
    )
    AssessmentAttempt.objects.filter(pk=attempt.pk).update(created_at=completed_at)

    scores_by_dimension_values = defaultdict(list)
    responses = []
    for question in assessment.questions.order_by("order"):
        score = _score_for(day_index, total_days, rng)
        responses.append(
            AssessmentResponse(
                attempt=attempt,
                user=user,
                assessment=assessment,
                question=question,
                score=score,
            )
        )
        scores_by_dimension_values[question.capital_dimension].append(score)

    AssessmentResponse.objects.bulk_create(responses)
    AssessmentResponse.objects.filter(attempt=attempt).update(created_at=completed_at)

    scores_by_dimension = {
        dimension: round(sum(values) / len(values), 2)
        for dimension, values in scores_by_dimension_values.items()
    }

    snapshot = AssessmentSnapshot.objects.create(
        attempt=attempt,
        user=user,
        assessment=assessment,
        scores_by_dimension=scores_by_dimension,
    )
    AssessmentSnapshot.objects.filter(pk=snapshot.pk).update(snapshot_date=date)
    return snapshot
