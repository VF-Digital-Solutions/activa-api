from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone

from apps.capitals.models import EmotionalLog

TREND_THRESHOLD = 0.5


def calculate_emotional_aggregates(user, window_days=7, as_of_date=None):
    """Agregados de EmotionalLog en una ventana de días: intensidad promedio,
    emociones dominantes y dirección de tendencia. Insumo para el módulo de
    insight (IVI).

    La tendencia compara el promedio de intensidad de la primera mitad de la
    ventana contra la segunda mitad; requiere datos en ambas mitades, de lo
    contrario es INSUFFICIENT_DATA.

    `as_of_date` permite recalcular la ventana como si se hubiera evaluado en
    una fecha pasada (usado por el seed de datos de demo); por defecto usa
    hoy, igual que antes.
    """
    end_date = as_of_date or timezone.localdate()
    start_date = end_date - timedelta(days=window_days - 1)

    logs = EmotionalLog.objects.filter(
        user=user, recorded_at__date__gte=start_date, recorded_at__date__lte=end_date
    )

    average_intensity = logs.aggregate(avg=Avg("intensity"))["avg"]
    average_intensity = (
        round(average_intensity, 2) if average_intensity is not None else None
    )

    emotion_counts = list(
        logs.values("emotion")
        .annotate(count=Count("id"))
        .order_by("-count", "emotion")
    )
    dominant_emotions = [item["emotion"] for item in emotion_counts[:3]]

    half = window_days // 2
    older_end = start_date + timedelta(days=half - 1)
    newer_start = older_end + timedelta(days=1)

    older_avg = logs.filter(recorded_at__date__lte=older_end).aggregate(
        avg=Avg("intensity")
    )["avg"]
    newer_avg = logs.filter(recorded_at__date__gte=newer_start).aggregate(
        avg=Avg("intensity")
    )["avg"]

    if older_avg is None or newer_avg is None:
        trend_direction = "INSUFFICIENT_DATA"
    else:
        diff = newer_avg - older_avg
        if diff > TREND_THRESHOLD:
            trend_direction = "IMPROVING"
        elif diff < -TREND_THRESHOLD:
            trend_direction = "DECLINING"
        else:
            trend_direction = "STABLE"

    return {
        "window_days": window_days,
        "start_date": start_date,
        "end_date": end_date,
        "total_entries": logs.count(),
        "average_intensity": average_intensity,
        "emotion_counts": emotion_counts,
        "dominant_emotions": dominant_emotions,
        "trend_direction": trend_direction,
    }
