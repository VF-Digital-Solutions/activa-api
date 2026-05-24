from django.urls import path
from apps.reservations.views import (
    ReservationCategoryListView,
    ReservationListCreateView,
    ReservationDetailView,
    ReservationDocumentListCreateView,
    ReservationStatusUpdateView,
)

urlpatterns = [
    path(
        "categories/",
        ReservationCategoryListView.as_view(),
        name="reservation-categories",
    ),
    path("", ReservationListCreateView.as_view(), name="reservation-list-create"),
    path("<uuid:pk>/", ReservationDetailView.as_view(), name="reservation-detail"),
    path(
        "<uuid:pk>/documents/",
        ReservationDocumentListCreateView.as_view(),
        name="reservation-documents",
    ),
    path(
        "<uuid:pk>/status/",
        ReservationStatusUpdateView.as_view(),
        name="reservation-status",
    ),
]
