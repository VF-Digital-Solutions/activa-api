from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.routines.models import (
    Habit,
    HabitLog,
    HabitStreak,
    HouseholdRoutine,
    HouseholdRoutineOccurrence,
)
from apps.routines.serializers import (
    HabitSerializer,
    HabitLogSerializer,
    HabitStreakSerializer,
    HouseholdRoutineSerializer,
    HouseholdRoutineOccurrenceSerializer,
)


@extend_schema(tags=["Routines - Habits"])
class HabitListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List habits",
        description="Returns all active habits for the authenticated user.",
        responses={200: HabitSerializer(many=True)},
    )
    def get(self, request):
        habits = Habit.objects.filter(user=request.user, is_active=True)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create habit",
        description="Creates a new habit for the authenticated user.",
        request=HabitSerializer,
        responses={201: HabitSerializer},
    )
    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Routines - Habits"])
class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Habit.objects.get(pk=pk, user=user, is_active=True)
        except Habit.DoesNotExist:
            return None

    @extend_schema(
        summary="Get habit",
        description="Returns a habit by ID.",
        responses={200: HabitSerializer},
    )
    def get(self, request, pk):
        habit = self.get_object(pk, request.user)
        if not habit:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(HabitSerializer(habit).data)

    @extend_schema(
        summary="Update habit",
        description="Partially updates a habit.",
        request=HabitSerializer,
        responses={200: HabitSerializer},
    )
    def patch(self, request, pk):
        habit = self.get_object(pk, request.user)
        if not habit:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HabitSerializer(habit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete habit",
        description="Soft deletes a habit.",
        responses={204: None},
    )
    def delete(self, request, pk):
        habit = self.get_object(pk, request.user)
        if not habit:
            return Response(status=status.HTTP_404_NOT_FOUND)
        habit.is_active = False
        habit.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Routines - Habits"])
class HabitLogCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Log habit",
        description="Records a daily log entry for a habit.",
        request=HabitLogSerializer,
        responses={201: HabitLogSerializer},
    )
    def post(self, request, pk):
        try:
            habit = Habit.objects.get(pk=pk, user=request.user, is_active=True)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["habit"] = habit.id
        serializer = HabitLogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(logged_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Routines - Habits"])
class HabitStreakView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get habit streak",
        description="Returns the current and longest streak for a habit.",
        responses={200: HabitStreakSerializer},
    )
    def get(self, request, pk):
        try:
            habit = Habit.objects.get(pk=pk, user=request.user, is_active=True)
            streak, _ = HabitStreak.objects.get_or_create(habit=habit)
            return Response(HabitStreakSerializer(streak).data)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Routines - Household"])
class HouseholdRoutineListCreate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List household routines",
        description="Returns all active routines for a household.",
        responses={200: HouseholdRoutineSerializer(many=True)},
    )
    def get(self, request):
        household_id = request.query_params.get("household")
        routines = HouseholdRoutine.objects.filter(is_active=True)
        if household_id:
            routines = routines.filter(household_node_id=household_id)
        serializer = HouseholdRoutineSerializer(routines, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create household routine",
        description="Creates a new routine for a household.",
        request=HouseholdRoutineSerializer,
        responses={201: HouseholdRoutineSerializer},
    )
    def post(self, request):
        serializer = HouseholdRoutineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Routines - Household"])
class HouseholdRoutineDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return HouseholdRoutine.objects.get(pk=pk, is_active=True)
        except HouseholdRoutine.DoesNotExist:
            return None

    @extend_schema(
        summary="Get household routine",
        description="Returns a household routine by ID.",
        responses={200: HouseholdRoutineSerializer},
    )
    def get(self, request, pk):
        routine = self.get_object(pk)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(HouseholdRoutineSerializer(routine).data)

    @extend_schema(
        summary="Update household routine",
        description="Partially updates a household routine.",
        request=HouseholdRoutineSerializer,
        responses={200: HouseholdRoutineSerializer},
    )
    def patch(self, request, pk):
        routine = self.get_object(pk)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HouseholdRoutineSerializer(routine, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete household routine",
        description="Soft deletes a household routine.",
        responses={204: None},
    )
    def delete(self, request, pk):
        routine = self.get_object(pk)
        if not routine:
            return Response(status=status.HTTP_404_NOT_FOUND)
        routine.is_active = False
        routine.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Routines - Household"])
class HouseholdRoutineOccurrenceListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List routine occurrences",
        description="Returns all occurrences for a household routine.",
        responses={200: HouseholdRoutineOccurrenceSerializer(many=True)},
    )
    def get(self, request, pk):
        occurrences = HouseholdRoutineOccurrence.objects.filter(routine_id=pk)
        serializer = HouseholdRoutineOccurrenceSerializer(occurrences, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Routines - Household"])
class HouseholdRoutineOccurrenceCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Complete occurrence",
        description="Marks a routine occurrence as completed.",
        responses={200: HouseholdRoutineOccurrenceSerializer},
    )
    def post(self, request, pk):
        try:
            occurrence = HouseholdRoutineOccurrence.objects.get(pk=pk)
        except HouseholdRoutineOccurrence.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        occurrence.status = HouseholdRoutineOccurrence.Status.COMPLETED
        occurrence.completed_at = timezone.now()
        occurrence.completed_by = request.user
        occurrence.save()
        return Response(HouseholdRoutineOccurrenceSerializer(occurrence).data)

