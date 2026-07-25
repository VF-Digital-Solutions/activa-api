"""Generador de TimeBlock para el seed de datos de demo."""

from datetime import datetime, time

from django.utils import timezone

from apps.agenda.models import TimeBlock
from apps.core.demo_data.config import WEEKDAY_BLOCK_PROFILE, WEEKEND_BLOCK_PROFILE

_TZ = timezone.get_current_timezone()


def _aware(date, hour, minute=0):
    return timezone.make_aware(datetime.combine(date, time(hour, minute)), _TZ)


def generate_time_blocks_for_day(user, date, rng, allow_planned=False):
    """Crea los TimeBlock del día según el perfil semana/finde de `config.py`.

    El status de cada bloque se resuelve con la probabilidad de
    `probability_fulfilled` del perfil: FULFILLED o OMITTED. Solo en días
    donde `allow_planned=True` (pensado para el último día del rango, que
    representa "hoy") algunos bloques quedan en PLANNED en vez de resueltos.
    """
    is_weekend = date.weekday() >= 5
    profile = WEEKEND_BLOCK_PROFILE if is_weekend else WEEKDAY_BLOCK_PROFILE

    blocks = []
    for title, category, energy_tag, duration, hour, probability_fulfilled in profile:
        if allow_planned and rng.random() < 0.25:
            status = TimeBlock.Status.PLANNED
        elif rng.random() < probability_fulfilled:
            status = TimeBlock.Status.FULFILLED
        else:
            status = TimeBlock.Status.OMITTED

        blocks.append(
            TimeBlock(
                user=user,
                title=title,
                existential_category=category,
                energy_tag=energy_tag,
                duration_minutes=duration,
                start_datetime=_aware(date, hour, rng.choice([0, 15, 30])),
                status=status,
            )
        )

    return TimeBlock.objects.bulk_create(blocks)
