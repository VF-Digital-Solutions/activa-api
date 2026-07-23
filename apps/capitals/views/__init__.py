from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.capitals.models import EmotionalLog, JournalEntry
from apps.capitals.serializers import EmotionalLogSerializer, JournalEntrySerializer


@extend_schema(tags=["Capitals"])
class EmotionalLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List emotional logs",
        description="Returns the authenticated user's emotional log entries.",
        responses={200: EmotionalLogSerializer(many=True)},
    )
    def get(self, request):
        logs = EmotionalLog.objects.filter(user=request.user)
        serializer = EmotionalLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Log an emotion",
        description=(
            "Creates an emotional log entry. Multiple entries per day are "
            "supported, each with its own recorded_at timestamp."
        ),
        request=EmotionalLogSerializer,
        responses={201: EmotionalLogSerializer},
    )
    def post(self, request):
        serializer = EmotionalLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Capitals"])
class EmotionalLogDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return EmotionalLog.objects.get(pk=pk, user=request.user)
        except EmotionalLog.DoesNotExist:
            return None

    @extend_schema(
        summary="Get emotional log",
        description="Returns an emotional log entry by ID.",
        responses={200: EmotionalLogSerializer},
    )
    def get(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(EmotionalLogSerializer(log).data)

    @extend_schema(
        summary="Update emotional log",
        description="Partially updates an emotional log entry.",
        request=EmotionalLogSerializer,
        responses={200: EmotionalLogSerializer},
    )
    def patch(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmotionalLogSerializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete emotional log",
        description="Deletes an emotional log entry.",
        responses={204: None},
    )
    def delete(self, request, pk):
        log = self.get_object(request, pk)
        if not log:
            return Response(status=status.HTTP_404_NOT_FOUND)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Capitals"])
class JournalEntryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List journal entries",
        description="Returns the authenticated user's journal entry history.",
        responses={200: JournalEntrySerializer(many=True)},
    )
    def get(self, request):
        entries = JournalEntry.objects.filter(user=request.user)
        serializer = JournalEntrySerializer(entries, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Log today's journal entry",
        description=(
            "Creates or updates the authenticated user's journal entry for "
            "today (one entry per calendar day)."
        ),
        request=JournalEntrySerializer,
        responses={200: JournalEntrySerializer, 201: JournalEntrySerializer},
    )
    def post(self, request):
        today = timezone.localdate()
        entry = JournalEntry.objects.filter(
            user=request.user, recorded_at__date=today
        ).first()
        created = entry is None

        serializer = JournalEntrySerializer(
            entry, data=request.data, partial=not created
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


@extend_schema(tags=["Capitals"])
class JournalEntryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return JournalEntry.objects.get(pk=pk, user=request.user)
        except JournalEntry.DoesNotExist:
            return None

    @extend_schema(
        summary="Get journal entry",
        description="Returns a journal entry by ID.",
        responses={200: JournalEntrySerializer},
    )
    def get(self, request, pk):
        entry = self.get_object(request, pk)
        if not entry:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(JournalEntrySerializer(entry).data)

    @extend_schema(
        summary="Update journal entry",
        description="Partially updates a journal entry.",
        request=JournalEntrySerializer,
        responses={200: JournalEntrySerializer},
    )
    def patch(self, request, pk):
        entry = self.get_object(request, pk)
        if not entry:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JournalEntrySerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete journal entry",
        description="Deletes a journal entry.",
        responses={204: None},
    )
    def delete(self, request, pk):
        entry = self.get_object(request, pk)
        if not entry:
            return Response(status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
