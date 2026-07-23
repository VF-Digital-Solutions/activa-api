from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.agenda_legacy.models import AgendaEvent
from apps.agenda_legacy.serializers import AgendaEventSerializer
from apps.identity.models import User
from apps.notifications.models import Alert


class AgendaEventListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = AgendaEvent.objects.filter(
            Q(user=request.user) | Q(attendees=request.user),
            is_active=True,
        ).distinct()
        serializer = AgendaEventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AgendaEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attendee_ids = serializer.validated_data.pop("attendee_ids", [])
        event = serializer.save(user=request.user)

        if attendee_ids:
            attendees = User.objects.filter(id__in=attendee_ids)
            event.attendees.set(attendees)
            self._notify_attendees(event, attendees, request.user)

        return Response(AgendaEventSerializer(event).data, status=status.HTTP_201_CREATED)

    def _notify_attendees(self, event, attendees, creator):
        alerts = [
            Alert(
                target_user=attendee,
                household_node=event.household_node,
                type=Alert.Type.CUSTOM,
                title=f"Evento: {event.title}",
                body=f"{creator.get_full_name() or creator.email} te invitó a '{event.title}'",
                action_url=f"/agenda",
                channels=["push"],
                scheduled_at=event.starts_at,
            )
            for attendee in attendees
            if attendee != creator
        ]
        Alert.objects.bulk_create(alerts)


class AgendaEventDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_event(self, pk, user):
        return AgendaEvent.objects.filter(
            Q(user=user) | Q(attendees=user),
            pk=pk,
            is_active=True,
        ).distinct().first()

    def get(self, request, pk):
        event = self._get_event(pk, request.user)
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(AgendaEventSerializer(event).data)

    def patch(self, request, pk):
        event = AgendaEvent.objects.filter(user=request.user, pk=pk, is_active=True).first()
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AgendaEventSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        attendee_ids = serializer.validated_data.pop("attendee_ids", None)
        updated = serializer.save()

        if attendee_ids is not None:
            attendees = User.objects.filter(id__in=attendee_ids)
            updated.attendees.set(attendees)

        return Response(AgendaEventSerializer(updated).data)

    def delete(self, request, pk):
        event = AgendaEvent.objects.filter(user=request.user, pk=pk, is_active=True).first()
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event.is_active = False
        event.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgendaEventInviteView(APIView):
    """Agregar o reemplazar los invitados de un evento del hogar."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        event = AgendaEvent.objects.filter(
            user=request.user, pk=pk, is_active=True, event_type=AgendaEvent.EventType.HOUSEHOLD
        ).first()
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)

        attendee_ids = request.data.get("attendee_ids", [])
        attendees = User.objects.filter(id__in=attendee_ids)
        existing_ids = set(event.attendees.values_list("id", flat=True))
        new_attendees = [u for u in attendees if u.id not in existing_ids]

        event.attendees.add(*attendees)

        if new_attendees:
            alerts = [
                Alert(
                    target_user=attendee,
                    household_node=event.household_node,
                    type=Alert.Type.CUSTOM,
                    title=f"Evento: {event.title}",
                    body=f"{request.user.get_full_name() or request.user.email} te invitó a '{event.title}'",
                    action_url="/agenda",
                    channels=["push"],
                    scheduled_at=event.starts_at,
                )
                for attendee in new_attendees
            ]
            Alert.objects.bulk_create(alerts)

        return Response(AgendaEventSerializer(event).data)
