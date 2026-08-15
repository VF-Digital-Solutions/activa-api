from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.health.models import SleepLog
from apps.health.serializers import SleepLogSerializer


@extend_schema(tags=["Health"])
class SleepLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List sleep logs",
        description="Returns the authenticated user's sleep log history.",
        responses={200: SleepLogSerializer(many=True)},
    )
    def get(self, request):
        logs = SleepLog.objects.filter(user=request.user)
        serializer = SleepLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Log sleep for a date",
        description=(
            "Creates or updates the authenticated user's sleep log for the "
            "given sleep_date (one entry per calendar date; defaults to "
            "today if omitted)."
        ),
        request=SleepLogSerializer,
        responses={200: SleepLogSerializer, 201: SleepLogSerializer},
    )
    def post(self, request):
        sleep_date = request.data.get("sleep_date") or timezone.localdate()
        entry = SleepLog.objects.filter(
            user=request.user, sleep_date=sleep_date
        ).first()
        created = entry is None

        serializer = SleepLogSerializer(entry, data=request.data, partial=not created)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


@extend_schema(tags=["Health"])
class SleepLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return SleepLog.objects.get(pk=pk, user=request.user)
        except SleepLog.DoesNotExist:
            return None

    @extend_schema(
        summary="Get sleep log",
        description="Returns a sleep log entry by ID.",
        responses={200: SleepLogSerializer},
    )
    def get(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(SleepLogSerializer(log).data)

    @extend_schema(
        summary="Update sleep log",
        description="Partially updates a sleep log entry.",
        request=SleepLogSerializer,
        responses={200: SleepLogSerializer},
    )
    def patch(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SleepLogSerializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete sleep log",
        description="Deletes a sleep log entry.",
        responses={204: None},
    )
    def delete(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
