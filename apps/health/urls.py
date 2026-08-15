from django.urls import path

from apps.health.views import (
    ActivityLogDetailView,
    ActivityLogListCreateView,
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
]
