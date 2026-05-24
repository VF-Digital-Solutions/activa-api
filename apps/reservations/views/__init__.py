from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.reservations.models import (
    Reservation,
    ReservationCategory,
    ReservationReminder,
    ReservationDocument,
)
from apps.reservations.serializers import (
    ReservationSerializer,
    ReservationCategorySerializer,
    ReservationReminderSerializer,
    ReservationDocumentSerializer,
)


@extend_schema(tags=["Reservations"])
class ReservationCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List reservation categories",
        description="Returns all available reservation categories.",
        responses={200: ReservationCategorySerializer(many=True)},
    )
    def get(self, request):
        categories = ReservationCategory.objects.all()
        serializer = ReservationCategorySerializer(categories, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Reservations"])
class ReservationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List reservations",
        description="Returns all reservations for the authenticated user. Filter by household using ?household=<id>.",
        responses={200: ReservationSerializer(many=True)},
    )
    def get(self, request):
        household_id = request.query_params.get("household")
        reservations = Reservation.objects.filter(user=request.user, is_active=True)
        if household_id:
            reservations = reservations.filter(household_node_id=household_id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create reservation",
        description="Creates a new reservation and automatically generates reminders.",
        request=ReservationSerializer,
        responses={201: ReservationSerializer},
    )
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save(user=request.user)

        # Crear recordatorio automático 24 horas antes
        ReservationReminder.objects.create(
            reservation=reservation,
            remind_at=reservation.starts_at - timedelta(hours=24),
            channels=["push", "email"],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Reservations"])
class ReservationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Reservation.objects.get(pk=pk, user=user, is_active=True)
        except Reservation.DoesNotExist:
            return None

    @extend_schema(
        summary="Get reservation",
        description="Returns a reservation by ID.",
        responses={200: ReservationSerializer},
    )
    def get(self, request, pk):
        reservation = self.get_object(pk, request.user)
        if not reservation:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ReservationSerializer(reservation).data)

    @extend_schema(
        summary="Update reservation",
        description="Partially updates a reservation.",
        request=ReservationSerializer,
        responses={200: ReservationSerializer},
    )
    def patch(self, request, pk):
        reservation = self.get_object(pk, request.user)
        if not reservation:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete reservation",
        description="Soft deletes a reservation.",
        responses={204: None},
    )
    def delete(self, request, pk):
        reservation = self.get_object(pk, request.user)
        if not reservation:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reservation.is_active = False
        reservation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Reservations"])
class ReservationDocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List reservation documents",
        description="Returns all documents attached to a reservation.",
        responses={200: ReservationDocumentSerializer(many=True)},
    )
    def get(self, request, pk):
        documents = ReservationDocument.objects.filter(reservation_id=pk)
        serializer = ReservationDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Upload reservation document",
        description="Attaches a new document to a reservation.",
        request=ReservationDocumentSerializer,
        responses={201: ReservationDocumentSerializer},
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["reservation"] = pk
        serializer = ReservationDocumentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Reservations"])
class ReservationStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update reservation status",
        description="Updates the status of a reservation (confirmed, completed, cancelled, no_show).",
        request={
            "application/json": {
                "type": "object",
                "properties": {"status": {"type": "string"}},
            }
        },
        responses={200: ReservationSerializer},
    )
    def patch(self, request, pk):
        try:
            reservation = Reservation.objects.get(
                pk=pk, user=request.user, is_active=True
            )
        except Reservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get("status")
        if new_status not in Reservation.Status.values:
            return Response(
                {"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST
            )
        reservation.status = new_status
        reservation.save()
        return Response(ReservationSerializer(reservation).data)
