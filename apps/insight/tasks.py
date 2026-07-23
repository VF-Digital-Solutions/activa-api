from celery import shared_task
from django.utils import timezone

from apps.identity.models import User
from apps.insight.models import IVISnapshot
from apps.insight.services import calculate_ivi


@shared_task
def compute_daily_ivi_snapshots():
    """Calcula y guarda el snapshot diario de IVI para cada usuario activo.

    Usuarios sin ambas evaluaciones base completadas (calculate_ivi
    retorna None) se omiten. Idempotente: repetir el mismo día actualiza
    el snapshot existente en vez de duplicarlo.
    """
    today = timezone.localdate()
    computed = 0

    for user in User.objects.filter(is_active=True):
        result = calculate_ivi(user)
        if result is None:
            continue

        IVISnapshot.objects.update_or_create(
            user=user,
            snapshot_date=today,
            defaults={
                "ivi": result["ivi"],
                "assets": result["assets"],
                "liabilities": result["liabilities"],
                "adaptation": result["adaptation"],
                "assets_by_dimension": result["assets_by_dimension"],
            },
        )
        computed += 1

    return computed
