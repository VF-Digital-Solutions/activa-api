from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.notifications.models import Alert
from apps.notifications.serializers import AlertSerializer
from apps.notifications.services import AlertService


@extend_schema(tags=["Notifications"])
class AlertListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List alerts",
        description="Returns all alerts for the authenticated user. Filter by status using ?status=PENDING|SENT|READ.",
        responses={200: AlertSerializer(many=True)},
    )
    def get(self, request):
        alert_status = request.query_params.get("status")
        alerts = Alert.objects.filter(target_user=request.user)
        if alert_status:
            alerts = alerts.filter(status=alert_status)
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Notifications"])
class AlertDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Alert.objects.get(pk=pk, target_user=user)
        except Alert.DoesNotExist:
            return None

    @extend_schema(
        summary="Get alert",
        description="Returns an alert by ID.",
        responses={200: AlertSerializer},
    )
    def get(self, request, pk):
        alert = self.get_object(pk, request.user)
        if not alert:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(AlertSerializer(alert).data)


@extend_schema(tags=["Notifications"])
class AlertMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Mark alert as read",
        description="Marks an alert as read.",
        responses={200: AlertSerializer},
    )
    def post(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk, target_user=request.user)
        except Alert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        alert = AlertService.mark_as_read(alert)
        return Response(AlertSerializer(alert).data)


@extend_schema(tags=["Notifications"])
class AlertMarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Mark all alerts as read",
        description="Marks all unread alerts as read for the authenticated user.",
        responses={
            200: {"type": "object", "properties": {"marked_read": {"type": "integer"}}}
        },
    )
    def post(self, request):
        alerts = Alert.objects.filter(
            target_user=request.user, status=Alert.Status.SENT
        )
        count = alerts.count()
        alerts.update(status=Alert.Status.READ, read_at=timezone.now())
        return Response({"marked_read": count})


@extend_schema(tags=["Notifications"])
class UnreadAlertCountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get unread alert count",
        description="Returns the count of unread alerts for the authenticated user.",
        responses={
            200: {"type": "object", "properties": {"unread_count": {"type": "integer"}}}
        },
    )
    def get(self, request):
        count = Alert.objects.filter(
            target_user=request.user,
            status__in=[Alert.Status.PENDING, Alert.Status.SENT],
        ).count()
        return Response({"unread_count": count})
