from django.urls import path
from apps.agenda_legacy.views import (
    AgendaView,
    AgendaTodayView,
    AgendaEventListCreateView,
    AgendaEventDetailView,
    AgendaEventInviteView,
)

urlpatterns = [
    path("", AgendaView.as_view(), name="agenda"),
    path("today/", AgendaTodayView.as_view(), name="agenda-today"),
    path("events/", AgendaEventListCreateView.as_view(), name="agenda-events"),
    path("events/<uuid:pk>/", AgendaEventDetailView.as_view(), name="agenda-event-detail"),
    path("events/<uuid:pk>/invite/", AgendaEventInviteView.as_view(), name="agenda-event-invite"),
]
