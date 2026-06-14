from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetDocument,
    AssetUsageLog,
    MaintenanceRecord,
    MaintenanceTemplate,
)
from apps.assets.serializers import (
    AssetSerializer,
    AssetCategorySerializer,
    AssetDocumentSerializer,
    AssetUsageLogSerializer,
    MaintenanceRecordSerializer,
    MaintenanceTemplateSerializer,
)


@extend_schema(tags=["Assets"])
class AssetCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List asset categories",
        description="Returns all top-level asset categories",
    )
    def get(self, request):
        categories = AssetCategory.objects.filter(parent__isnull=True)
        serializer = AssetCategorySerializer(categories, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Assets"])
class AssetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List assets",
        description="Returns all assets. Filter by household using ?householdid=<id>.",
    )
    def get(self, request):
        household_id = request.query_params.get("household")
        assets = Asset.objects.filter(is_active=True)
        if household_id:
            assets = assets.filter(household_node_id=household_id)
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Assets"])
class AssetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk, is_active=True)
        except Asset.DoesNotExist:
            return None

    @extend_schema(
        summary="Get asset",
        description="Returns an asset by ID.",
    )
    def get(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(AssetSerializer(asset).data)

    @extend_schema(
        summary="Update asset",
        description="Partially updates an asset.",
    )
    def patch(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete asset",
        description="Soft deletesan asset.",
    )
    def delete(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        asset.is_active = False
        asset.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Assets"])
class AssetDocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List asset documents",
        description="Returns all documents attached to an asset..",
    )
    def get(self, request, pk):
        documents = AssetDocument.objects.filter(asset_id=pk)
        serializer = AssetDocumentSerializer(documents, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        summary="Upload asset document",
        description="Attaches a new document to an asset.",
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["asset"] = pk
        serializer = AssetDocumentSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Assets"])
class AssetUsageLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List usage logs",
        description="Returns all usage logs for an asset.",
    )
    def get(self, request, pk):
        logs = AssetUsageLog.objects.filter(asset_id=pk)
        serializer = AssetUsageLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create usage log",
        description="Records a new usage log entry for an asset.",
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["asset"] = pk
        serializer = AssetUsageLogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(recorded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Assets"])
class MaintenanceRecordListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List maintenance records",
        description="Returns all maintenance records for an asset.",
    )
    def get(self, request, pk):
        records = MaintenanceRecord.objects.filter(asset_id=pk)
        serializer = MaintenanceRecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data.copy()
        data["asset"] = pk
        serializer = MaintenanceRecordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Assets"])
class MaintenanceRecordDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MaintenanceRecord.objects.get(pk=pk)
        except MaintenanceRecord.DoesNotExist:
            return None

    @extend_schema(
        summary="Update maintenance record",
        description="Partially updates a maintenance record.",
    )
    def patch(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MaintenanceRecordSerializer(
            record, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@extend_schema(tags=["Assets"])
class MaintenanceTemplateListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List maintenance templates",
        description="Returns maintenance templates. Filter by category using ?category=<id>.",
        parameters=[
            OpenApiParameter("category", OpenApiTypes.UUID, description="Filter by category ID"),
        ],
    )
    def get(self, request):
        category_id = request.query_params.get("category")
        templates = MaintenanceTemplate.objects.all()
        if category_id:
            templates = templates.filter(category_id=category_id)
        serializer = MaintenanceTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create maintenance template",
        description="Creates a new maintenance template for a category.",
    )
    def post(self, request):
        serializer = MaintenanceTemplateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Assets"])
class MaintenanceTemplateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MaintenanceTemplate.objects.get(pk=pk)
        except MaintenanceTemplate.DoesNotExist:
            return None

    @extend_schema(summary="Get maintenance template")
    def get(self, request, pk):
        template = self.get_object(pk)
        if not template:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(MaintenanceTemplateSerializer(template).data)

    @extend_schema(summary="Update maintenance template")
    def patch(self, request, pk):
        template = self.get_object(pk)
        if not template:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MaintenanceTemplateSerializer(template, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Delete maintenance template")
    def delete(self, request, pk):
        template = self.get_object(pk)
        if not template:
            return Response(status=status.HTTP_404_NOT_FOUND)
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
