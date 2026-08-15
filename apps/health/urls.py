from django.urls import path

from apps.health.views import (
    ActivityLogDetailView,
    ActivityLogListCreateView,
    BiometricLogDetailView,
    BiometricLogListCreateView,
    MedicationDetailView,
    MedicationDoseLogListCreateView,
    MedicationListCreateView,
    NutritionLogDetailView,
    NutritionLogListCreateView,
    SleepLogDetailView,
    SleepLogListCreateView,
)

urlpatterns = [
    path("sleep-logs/", SleepLogListCreateView.as_view(), name="sleep-log-list-create"),
    path("sleep-logs/<uuid:pk>/", SleepLogDetailView.as_view(), name="sleep-log-detail"),
    path(
        "activity-logs/",
        ActivityLogListCreateView.as_view(),
        name="activity-log-list-create",
    ),
    path(
        "activity-logs/<uuid:pk>/",
        ActivityLogDetailView.as_view(),
        name="activity-log-detail",
    ),
    path(
        "nutrition-logs/",
        NutritionLogListCreateView.as_view(),
        name="nutrition-log-list-create",
    ),
    path(
        "nutrition-logs/<uuid:pk>/",
        NutritionLogDetailView.as_view(),
        name="nutrition-log-detail",
    ),
    path("medications/", MedicationListCreateView.as_view(), name="medication-list-create"),
    path(
        "medications/<uuid:pk>/",
        MedicationDetailView.as_view(),
        name="medication-detail",
    ),
    path(
        "medication-dose-logs/",
        MedicationDoseLogListCreateView.as_view(),
        name="medication-dose-log-list-create",
    ),
    path(
        "biometric-logs/",
        BiometricLogListCreateView.as_view(),
        name="biometric-log-list-create",
    ),
    path(
        "biometric-logs/<uuid:pk>/",
        BiometricLogDetailView.as_view(),
        name="biometric-log-detail",
    ),
]
