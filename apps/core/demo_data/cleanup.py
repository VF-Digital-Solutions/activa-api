"""Borrado idempotente del rango de fechas sembrado por el seed de demo."""

from apps.agenda.models import TimeBlock
from apps.assessment.models import AssessmentAttempt, AssessmentSnapshot
from apps.capitals.models import EmotionalLog, JournalEntry
from apps.insight.models import IVISnapshot


def delete_existing_range(user, start_date, end_date):
    """Borra todo lo previamente sembrado para `user` en [start_date, end_date],
    para que el comando sea reejecutable sin duplicar datos.

    Los AssessmentAttempt se borran (no los Snapshot directamente) porque
    AssessmentResponse y AssessmentSnapshot cuelgan de Attempt con
    on_delete=CASCADE; borrar solo el snapshot dejaría huérfanos el attempt
    y sus respuestas.
    """
    TimeBlock.objects.filter(
        user=user,
        start_datetime__date__gte=start_date,
        start_datetime__date__lte=end_date,
    ).delete()

    EmotionalLog.objects.filter(
        user=user,
        recorded_at__date__gte=start_date,
        recorded_at__date__lte=end_date,
    ).delete()

    JournalEntry.objects.filter(
        user=user,
        recorded_at__date__gte=start_date,
        recorded_at__date__lte=end_date,
    ).delete()

    IVISnapshot.objects.filter(
        user=user,
        snapshot_date__gte=start_date,
        snapshot_date__lte=end_date,
    ).delete()

    attempt_ids = list(
        AssessmentSnapshot.objects.filter(
            user=user,
            snapshot_date__gte=start_date,
            snapshot_date__lte=end_date,
        ).values_list("attempt_id", flat=True)
    )
    AssessmentAttempt.objects.filter(id__in=attempt_ids).delete()
