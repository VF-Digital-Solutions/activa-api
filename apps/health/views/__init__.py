from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.health.models import (
    ActivityLog,
    Medication,
    MedicationDoseLog,
    NutritionLog,
    SleepLog,
)
from apps.health.serializers import (
    ActivityLogSerializer,
    MedicationDoseLogSerializer,
    MedicationSerializer,
    NutritionLogSerializer,
    SleepLogSerializer,
)


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


@extend_schema(tags=["Health"])
class ActivityLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List activity logs",
        description="Returns the authenticated user's physical activity log history.",
        responses={200: ActivityLogSerializer(many=True)},
    )
    def get(self, request):
        logs = ActivityLog.objects.filter(user=request.user)
        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Log a physical activity session",
        description=(
            "Creates an activity log entry. Multiple entries per day are "
            "supported, each with its own recorded_at timestamp."
        ),
        request=ActivityLogSerializer,
        responses={201: ActivityLogSerializer},
    )
    def post(self, request):
        serializer = ActivityLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Health"])
class ActivityLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return ActivityLog.objects.get(pk=pk, user=request.user)
        except ActivityLog.DoesNotExist:
            return None

    @extend_schema(
        summary="Get activity log",
        description="Returns an activity log entry by ID.",
        responses={200: ActivityLogSerializer},
    )
    def get(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ActivityLogSerializer(log).data)

    @extend_schema(
        summary="Update activity log",
        description="Partially updates an activity log entry.",
        request=ActivityLogSerializer,
        responses={200: ActivityLogSerializer},
    )
    def patch(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActivityLogSerializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete activity log",
        description="Deletes an activity log entry.",
        responses={204: None},
    )
    def delete(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Health"])
class NutritionLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List nutrition logs",
        description="Returns the authenticated user's nutrition log history.",
        responses={200: NutritionLogSerializer(many=True)},
    )
    def get(self, request):
        logs = NutritionLog.objects.filter(user=request.user)
        serializer = NutritionLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Log a meal",
        description=(
            "Creates a nutrition log entry. Multiple entries per day are "
            "supported, each with its own recorded_at timestamp."
        ),
        request=NutritionLogSerializer,
        responses={201: NutritionLogSerializer},
    )
    def post(self, request):
        serializer = NutritionLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Health"])
class NutritionLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return NutritionLog.objects.get(pk=pk, user=request.user)
        except NutritionLog.DoesNotExist:
            return None

    @extend_schema(
        summary="Get nutrition log",
        description="Returns a nutrition log entry by ID.",
        responses={200: NutritionLogSerializer},
    )
    def get(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(NutritionLogSerializer(log).data)

    @extend_schema(
        summary="Update nutrition log",
        description="Partially updates a nutrition log entry.",
        request=NutritionLogSerializer,
        responses={200: NutritionLogSerializer},
    )
    def patch(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = NutritionLogSerializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete nutrition log",
        description="Deletes a nutrition log entry.",
        responses={204: None},
    )
    def delete(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Health"])
class MedicationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List medications",
        description="Returns the authenticated user's medications.",
        responses={200: MedicationSerializer(many=True)},
    )
    def get(self, request):
        medications = Medication.objects.filter(user=request.user)
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add a medication",
        description="Creates a medication with its dosage, frequency and reminder times.",
        request=MedicationSerializer,
        responses={201: MedicationSerializer},
    )
    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Health"])
class MedicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return Medication.objects.get(pk=pk, user=request.user)
        except Medication.DoesNotExist:
            return None

    @extend_schema(
        summary="Get medication",
        description="Returns a medication by ID.",
        responses={200: MedicationSerializer},
    )
    def get(self, request, pk):
        medication = self.get_object(request, pk)
        if not medication:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(MedicationSerializer(medication).data)

    @extend_schema(
        summary="Update medication",
        description="Partially updates a medication (e.g. deactivate it).",
        request=MedicationSerializer,
        responses={200: MedicationSerializer},
    )
    def patch(self, request, pk):
        medication = self.get_object(request, pk)
        if not medication:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MedicationSerializer(medication, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete medication",
        description="Deletes a medication and its dose history.",
        responses={204: None},
    )
    def delete(self, request, pk):
        medication = self.get_object(request, pk)
        if not medication:
            return Response(status=status.HTTP_404_NOT_FOUND)
        medication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Health"])
class MedicationDoseLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List medication dose logs",
        description="Returns the authenticated user's medication dose history.",
        responses={200: MedicationDoseLogSerializer(many=True)},
    )
    def get(self, request):
        logs = MedicationDoseLog.objects.filter(user=request.user)
        serializer = MedicationDoseLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Log a medication dose",
        description="Records that a dose was taken or skipped.",
        request=MedicationDoseLogSerializer,
        responses={201: MedicationDoseLogSerializer},
    )
    def post(self, request):
        serializer = MedicationDoseLogSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
