from django.urls import path

from apps.capitals.views import (
    EmotionalLogDetailView,
    EmotionalLogListCreateView,
    JournalEntryDetailView,
    JournalEntryListCreateView,
)

urlpatterns = [
    path(
        "emotional-logs/",
        EmotionalLogListCreateView.as_view(),
        name="emotional-log-list-create",
    ),
    path(
        "emotional-logs/<uuid:pk>/",
        EmotionalLogDetailView.as_view(),
        name="emotional-log-detail",
    ),
    path(
        "journal-entries/",
        JournalEntryListCreateView.as_view(),
        name="journal-entry-list-create",
    ),
    path(
        "journal-entries/<uuid:pk>/",
        JournalEntryDetailView.as_view(),
        name="journal-entry-detail",
    ),
]
