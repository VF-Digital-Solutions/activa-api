from django.urls import path

from apps.agenda.views import (
    DayCloseView,
    TimeBlockDetailView,
    TimeBlockListCreateView,
)

urlpatterns = [
    path("", TimeBlockListCreateView.as_view(), name="time-block-list-create"),
    path("<uuid:pk>/", TimeBlockDetailView.as_view(), name="time-block-detail"),
    path("day-close/", DayCloseView.as_view(), name="agenda-day-close"),
]
