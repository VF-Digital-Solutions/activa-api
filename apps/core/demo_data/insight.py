"""Persistencia de IVISnapshot para el seed de demo, usando la fórmula real."""

from apps.insight.models import IVISnapshot
from apps.insight.services import calculate_ivi


def seed_ivi_snapshot_for_day(user, date):
    """Calcula el IVI "como si" se hubiera evaluado en `date` (usando la
    función real de negocio, `calculate_ivi(user, as_of_date=date)`) y lo
    persiste. No crea nada si todavía faltan evaluaciones base para esa
    fecha (mismo comportamiento que la task de Celery en producción)."""
    result = calculate_ivi(user, as_of_date=date)
    if result is None:
        return None

    snapshot, _ = IVISnapshot.objects.update_or_create(
        user=user,
        snapshot_date=date,
        defaults={
            "ivi": result["ivi"],
            "assets": result["assets"],
            "liabilities": result["liabilities"],
            "adaptation": result["adaptation"],
            "assets_by_dimension": result["assets_by_dimension"],
        },
    )
    return snapshot
