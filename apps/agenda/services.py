from django.db.models import Q

from apps.agenda.models import TimeBlock

DEFAULT_SLEEP_HOURS = 8
UNASSIGNED = "UNASSIGNED"


def calculate_daily_distribution(user, date, sleep_hours=DEFAULT_SLEEP_HOURS):
    """Distribución diaria de bloques cumplidos por categoría existencial y energía.

    El denominador son las horas de vigilia (24 - horas de sueño). El tiempo
    no cubierto por ningún bloque cumplido se reporta en un bucket neutral
    "UNASSIGNED", nunca como tiempo perdido.

    Un bloque se atribuye a `date` según su start_datetime; si no tiene
    start_datetime (registro retroactivo), se atribuye según la fecha en que
    fue creado.
    """
    waking_minutes = max(24 - sleep_hours, 0) * 60

    blocks = TimeBlock.objects.filter(
        user=user, status=TimeBlock.Status.FULFILLED
    ).filter(
        Q(start_datetime__date=date)
        | Q(start_datetime__isnull=True, created_at__date=date)
    )

    by_category = {category: 0 for category in TimeBlock.ExistentialCategory.values}
    by_energy_tag = {tag: 0 for tag in TimeBlock.EnergyTag.values}

    for block in blocks:
        by_category[block.existential_category] += block.duration_minutes
        by_energy_tag[block.energy_tag] += block.duration_minutes

    assigned_minutes = sum(by_category.values())
    unassigned_minutes = max(waking_minutes - assigned_minutes, 0)

    by_category[UNASSIGNED] = unassigned_minutes
    by_energy_tag[UNASSIGNED] = unassigned_minutes

    return {
        "date": date,
        "waking_minutes": waking_minutes,
        "assigned_minutes": assigned_minutes,
        "unassigned_minutes": unassigned_minutes,
        "by_category": by_category,
        "by_energy_tag": by_energy_tag,
    }
