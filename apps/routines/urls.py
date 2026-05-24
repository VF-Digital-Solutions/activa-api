from django.urls import path
from apps.routines.views import (
    HabitListCreateView,
    HabitDetailView,
    HabitLogCreateView,
    HabitStreakView,
    HouseholdRoutineListCreateView,
    HouseholdRoutineDetailView,
    HouseholdRoutineOccurrenceListView,
    HouseholdRoutineOccurrenceCompleteView,
)

urlpatterns = [
    # Habits
    path("habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    path("habits/<uuid:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("habits/<uuid:pk>/log/", HabitLogCreateView.as_view(), name="habit-log"),
    path("habits/<uuid:pk>/streak/", HabitStreakView.as_view(), name="habit-streak"),
    # Household Routines
    path(
        "household/",
        HouseholdRoutineListCreateView.as_view(),
        name="household-routine-list-create",
    ),
    path(
        "household/<uuid:pk>/",
        HouseholdRoutineDetailView.as_view(),
        name="household-routine-detail",
    ),
    path(
        "household/<uuid:pk>/occurrences/",
        HouseholdRoutineOccurrenceListView.as_view(),
        name="household-routine-occurrences",
    ),
    path(
        "occurrences/<uuid:pk>/complete/",
        HouseholdRoutineOccurrenceCompleteView.as_view(),
        name="occurrence-complete",
    ),
]
