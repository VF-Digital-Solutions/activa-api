from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.capitals.models import EmotionalLog
from apps.capitals.serializers import EmotionalLogSerializer


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
