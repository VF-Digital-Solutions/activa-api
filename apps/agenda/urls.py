from django.urls import path

from apps.agenda.views import TimeBlockDetailView, TimeBlockListCreateView

urlpatterns = [
    path("", TimeBlockListCreateView.as_view(), name="time-block-list-create"),
    path("<uuid:pk>/", TimeBlockDetailView.as_view(), name="time-block-detail"),
]
