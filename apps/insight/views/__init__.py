from datetime import timedelta

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.insight.models import IVISnapshot
from apps.insight.serializers import IVISnapshotSerializer, IVITrendsQuerySerializer


@extend_schema(tags=["Insight"])
class IVITrendsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="IVI trends",
        description=(
            "Returns the authenticated user's IVI history for the last N "
            "days (default 90), ordered oldest to newest, with the "
            "per-dimension asset series for charting."
        ),
        parameters=[IVITrendsQuerySerializer],
        responses={200: IVISnapshotSerializer(many=True)},
    )
    def get(self, request):
        query = IVITrendsQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        days = query.validated_data["days"]

        start_date = timezone.localdate() - timedelta(days=days - 1)
        snapshots = IVISnapshot.objects.filter(
            user=request.user, snapshot_date__gte=start_date
        ).order_by("snapshot_date")

        return Response(IVISnapshotSerializer(snapshots, many=True).data)
