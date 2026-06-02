from datetime import datetime
from django.utils import timezone
from apps.notifications.models import Alert


class AlertService:
    """
    Servicio central para crear alertas desde cualquier módulo.
    Uso:
        AlertService.schedule(
            user=user,
            type=Alert.Type.MAINTENANCE,
            source=maintenance_record,
            title="Mantenimiento programado",
            body="El service de tu auto vence el 01/06.",
            channels=["push", "email"],
            scheduled_at=datetime(2026, 5, 30, 9, 0),
        )
    """

    @staticmethod
    def schedule(
        user,
        type: str,
        title: str,
        body: str,
        scheduled_at: datetime,
        channels: list = None,
        source=None,
        household_node=None,
        action_url: str = "",
        metadata: dict = None,
    ) -> Alert:
        from django.contrib.contenttypes.models import ContentType

        if channels is None:
            channels = ["push", "email"]

        if metadata is None:
            metadata = {}

        content_type = None
        object_id = None

        if source is not None:
            content_type = ContentType.objects.get_for_model(source)
            object_id = source.id

        alert = Alert.objects.create(
            target_user=user,
            household_node=household_node,
            source_content_type=content_type,
            source_object_id=object_id,
            type=type,
            title=title,
            body=body,
            action_url=action_url,
            metadata=metadata,
            channels=channels,
            scheduled_at=scheduled_at,
            status=Alert.Status.PENDING,
        )

        return alert

    @staticmethod
    def mark_as_read(alert: Alert) -> Alert:
        alert.read_at = timezone.now()
        alert.status = Alert.Status.READ
        alert.save()
        return alert

    @staticmethod
    def cancel(alert: Alert) -> Alert:
        alert.status = Alert.Status.CANCELLED
        alert.save()
        return alert
