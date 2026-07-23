from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.agenda.models import TimeBlock
from apps.agenda.serializers import TimeBlockSerializer


@extend_schema(tags=["Agenda"])
class TimeBlockListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List time blocks",
        description=(
            "Returns the authenticated user's time blocks. "
            "Filter by status using ?status=<PLANNED|FULFILLED|OMITTED>."
        ),
        responses={200: TimeBlockSerializer(many=True)},
    )
    def get(self, request):
        blocks = TimeBlock.objects.filter(user=request.user)
        status_param = request.query_params.get("status")
        if status_param:
            blocks = blocks.filter(status=status_param)
        serializer = TimeBlockSerializer(blocks, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a time block",
        description=(
            "Creates a time block. Supports retroactive registration: pass "
            "status=FULFILLED and omit start_datetime to log unplanned time "
            "already lived, without prior planning."
        ),
        request=TimeBlockSerializer,
        responses={201: TimeBlockSerializer},
    )
    def post(self, request):
        serializer = TimeBlockSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Agenda"])
class TimeBlockDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return TimeBlock.objects.get(pk=pk, user=request.user)
        except TimeBlock.DoesNotExist:
            return None

    @extend_schema(
        summary="Get time block",
        description="Returns a time block by ID.",
        responses={200: TimeBlockSerializer},
    )
    def get(self, request, pk):
        block = self.get_object(request, pk)
        if not block:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(TimeBlockSerializer(block).data)

    @extend_schema(
        summary="Update time block",
        description="Partially updates a time block.",
        request=TimeBlockSerializer,
        responses={200: TimeBlockSerializer},
    )
    def patch(self, request, pk):
        block = self.get_object(request, pk)
        if not block:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TimeBlockSerializer(
            block, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete time block",
        description="Deletes a time block.",
        responses={204: None},
    )
    def delete(self, request, pk):
        block = self.get_object(request, pk)
        if not block:
            return Response(status=status.HTTP_404_NOT_FOUND)
        block.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
