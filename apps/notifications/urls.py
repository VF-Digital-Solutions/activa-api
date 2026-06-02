from django.urls import path
from apps.notifications.views import (
    AlertListView,
    AlertDetailView,
    AlertMarkReadView,
    AlertMarkAllReadView,
    UnreadAlertCountView,
)

urlpatterns = [
    path("", AlertListView.as_view(), name="alert-list"),
    path("<uuid:pk>/", AlertDetailView.as_view(), name="alert-detail"),
    path("<uuid:pk>/mark-read/", AlertMarkReadView.as_view(), name="alert-mark-read"),
    path("mark-all-read/", AlertMarkAllReadView.as_view(), name="alert-mark-all-read"),
    path("unread-count/", UnreadAlertCountView.as_view(), name="alert-unread-count"),
]
