import uuid
from datetime import datetime, timezone, timedelta
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.reservations.models import Reservation
from apps.routines.models import HouseholdRoutineOccurrence, Habit
from apps.agenda_legacy.models import AgendaEvent


# Colors por tipo de fuente
SOURCE_COLORS = {
    "reservation": "#C8A96B",
    "task": "#6B8FC8",
    "habit": "#6BC88F",
    "reminder": "#C86B6B",
    "event": "#A96BC8",
}


def _reservation_to_item(r):
    return {
        "id": uuid.uuid4(),
        "source": "reservation",
        "source_id": r.id,
        "type": r.type.lower() if r.type else "appointment",
        "title": r.title,
        "starts_at": r.starts_at,
        "ends_at": r.ends_at,
        "is_all_day": r.is_all_day,
        "status": r.status,
        "color": SOURCE_COLORS["reservation"],
        "metadata": {
            "location": r.location_name,
            "provider": r.provider_name,
            "meeting_url": r.meeting_url,
        },
    }


def _occurrence_to_item(o):
    return {
        "id": uuid.uuid4(),
        "source": "task",
        "source_id": o.id,
        "type": "task",
        "title": o.routine.title if o.routine_id else "Tarea",
        "starts_at": o.due_at,
        "ends_at": None,
        "is_all_day": False,
        "status": o.status,
        "color": SOURCE_COLORS["task"],
        "metadata": {
            "assigned_to": str(o.assigned_to_id) if o.assigned_to_id else None,
            "routine_id": str(o.routine_id) if o.routine_id else None,
        },
    }


def _agenda_event_to_item(e):
    source = "reminder" if e.event_type == AgendaEvent.EventType.REMINDER else "event"
    return {
        "id": uuid.uuid4(),
        "source": source,
        "source_id": e.id,
        "type": e.event_type.lower(),
        "title": e.title,
        "starts_at": e.starts_at,
        "ends_at": e.ends_at,
        "is_all_day": e.is_all_day,
        "status": None,
        "color": e.color or SOURCE_COLORS.get(source, "#888888"),
        "metadata": {
            "description": e.description,
            "household_node": str(e.household_node_id) if e.household_node_id else None,
            "created_by": str(e.user_id),
        },
    }


class AgendaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = datetime.now(tz=timezone.utc)
        from_dt = self._parse_dt(request.query_params.get("from"), now)
        to_dt = self._parse_dt(request.query_params.get("to"), now + timedelta(days=30))
        active_types = request.query_params.getlist("types") or [
            "reservation", "task", "habit", "event", "reminder"
        ]

        items = []

        if "reservation" in active_types:
            reservations = Reservation.objects.filter(
                user=request.user,
                starts_at__range=(from_dt, to_dt),
                is_active=True,
            )
            items += [_reservation_to_item(r) for r in reservations]

        if "task" in active_types:
            occurrences = HouseholdRoutineOccurrence.objects.filter(
                assigned_to=request.user,
                due_at__range=(from_dt, to_dt),
            ).select_related("routine")
            items += [_occurrence_to_item(o) for o in occurrences]

        if "event" in active_types or "reminder" in active_types:
            type_filter = []
            if "event" in active_types:
                type_filter += [AgendaEvent.EventType.PERSONAL, AgendaEvent.EventType.HOUSEHOLD]
            if "reminder" in active_types:
                type_filter.append(AgendaEvent.EventType.REMINDER)

            events = AgendaEvent.objects.filter(
                Q(user=request.user) | Q(attendees=request.user),
                starts_at__range=(from_dt, to_dt),
                is_active=True,
                event_type__in=type_filter,
            ).distinct()
            items += [_agenda_event_to_item(e) for e in events]

        items.sort(key=lambda x: x["starts_at"])
        return Response(items)

    def _parse_dt(self, value, default):
        if not value:
            return default
        try:
            dt = datetime.fromisoformat(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            return default


class AgendaTodayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = datetime.now(tz=timezone.utc)
        from_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        to_dt = from_dt + timedelta(days=1)
        active_types = request.query_params.getlist("types") or [
            "reservation", "task", "habit", "event", "reminder"
        ]

        items = []

        if "reservation" in active_types:
            reservations = Reservation.objects.filter(
                user=request.user,
                starts_at__range=(from_dt, to_dt),
                is_active=True,
            )
            items += [_reservation_to_item(r) for r in reservations]

        if "task" in active_types:
            occurrences = HouseholdRoutineOccurrence.objects.filter(
                assigned_to=request.user,
                due_at__range=(from_dt, to_dt),
            ).select_related("routine")
            items += [_occurrence_to_item(o) for o in occurrences]

        if "event" in active_types or "reminder" in active_types:
            type_filter = []
            if "event" in active_types:
                type_filter += [AgendaEvent.EventType.PERSONAL, AgendaEvent.EventType.HOUSEHOLD]
            if "reminder" in active_types:
                type_filter.append(AgendaEvent.EventType.REMINDER)

            events = AgendaEvent.objects.filter(
                Q(user=request.user) | Q(attendees=request.user),
                starts_at__range=(from_dt, to_dt),
                is_active=True,
                event_type__in=type_filter,
            ).distinct()
            items += [_agenda_event_to_item(e) for e in events]

        items.sort(key=lambda x: x["starts_at"])
        return Response(items)
