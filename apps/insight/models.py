from django.db import models

from apps.core.models import TimeStampedModel
from apps.identity.models import User


class IVISnapshot(TimeStampedModel):
    """Fotografía diaria del Índice Vital Integrado (IVI) de un usuario."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ivi_snapshots"
    )
    snapshot_date = models.DateField()
    ivi = models.FloatField()
    assets = models.FloatField()
    liabilities = models.FloatField()
    adaptation = models.FloatField()
    assets_by_dimension = models.JSONField(default=dict)

    class Meta:
        db_table = "insight_ivi_snapshot"
        verbose_name = "Snapshot de IVI"
        verbose_name_plural = "Snapshots de IVI"
        unique_together = ("user", "snapshot_date")
        ordering = ["-snapshot_date"]

    def __str__(self):
        return f"{self.user} — {self.snapshot_date}: {self.ivi}"
