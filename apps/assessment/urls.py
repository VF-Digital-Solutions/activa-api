from django.urls import path

from apps.assessment.views import (
    AssessmentAnswerView,
    AssessmentCompleteView,
    AssessmentEvolutionView,
    AssessmentStartView,
)

urlpatterns = [
    path("start/", AssessmentStartView.as_view(), name="assessment-start"),
    path(
        "attempts/<uuid:pk>/answer/",
        AssessmentAnswerView.as_view(),
        name="assessment-answer",
    ),
    path(
        "attempts/<uuid:pk>/complete/",
        AssessmentCompleteView.as_view(),
        name="assessment-complete",
    ),
    path(
        "evolution/",
        AssessmentEvolutionView.as_view(),
        name="assessment-evolution",
    ),
]
