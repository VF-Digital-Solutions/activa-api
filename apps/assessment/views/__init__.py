from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.assessment.models import (
    AssessmentAttempt,
    AssessmentResponse,
    AssessmentSnapshot,
    Question,
)
from apps.assessment.serializers import (
    AnswerSerializer,
    AssessmentAttemptSerializer,
    AssessmentResponseSerializer,
    AssessmentSnapshotSerializer,
    StartAssessmentSerializer,
)


@extend_schema(tags=["Assessment"])
class AssessmentStartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Start an assessment",
        description="Starts a new attempt on the latest version of the given assessment type.",
        request=StartAssessmentSerializer,
        responses={201: AssessmentAttemptSerializer},
    )
    def post(self, request):
        serializer = StartAssessmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attempt = AssessmentAttempt.objects.create(
            user=request.user, assessment=serializer.assessment
        )
        return Response(
            AssessmentAttemptSerializer(attempt).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Assessment"])
class AssessmentAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Answer a question",
        description="Records (or updates) the score for a question within an in-progress attempt.",
        request=AnswerSerializer,
        responses={200: AssessmentResponseSerializer},
    )
    def post(self, request, pk):
        attempt = get_object_or_404(
            AssessmentAttempt,
            pk=pk,
            user=request.user,
            status=AssessmentAttempt.Status.IN_PROGRESS,
        )
        serializer = AnswerSerializer(data=request.data, context={"attempt": attempt})
        serializer.is_valid(raise_exception=True)

        response, _ = AssessmentResponse.objects.update_or_create(
            attempt=attempt,
            question=serializer.validated_data["question"],
            defaults={
                "user": request.user,
                "assessment": attempt.assessment,
                "score": serializer.validated_data["score"],
            },
        )
        return Response(AssessmentResponseSerializer(response).data)


@extend_schema(tags=["Assessment"])
class AssessmentCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Complete an assessment",
        description=(
            "Finalizes an in-progress attempt: computes the average score per "
            "capital dimension from the recorded responses and stores it as a "
            "dated snapshot."
        ),
        responses={200: AssessmentSnapshotSerializer},
    )
    def post(self, request, pk):
        attempt = get_object_or_404(
            AssessmentAttempt,
            pk=pk,
            user=request.user,
            status=AssessmentAttempt.Status.IN_PROGRESS,
        )

        scores_by_dimension = {}
        for dimension in Question.CapitalDimension.values:
            average = attempt.responses.filter(
                question__capital_dimension=dimension
            ).aggregate(average=Avg("score"))["average"]
            if average is not None:
                scores_by_dimension[dimension] = round(average, 2)

        snapshot = AssessmentSnapshot.objects.create(
            attempt=attempt,
            user=request.user,
            assessment=attempt.assessment,
            scores_by_dimension=scores_by_dimension,
        )

        attempt.status = AssessmentAttempt.Status.COMPLETED
        attempt.completed_at = timezone.now()
        attempt.save(update_fields=["status", "completed_at"])

        return Response(AssessmentSnapshotSerializer(snapshot).data)
