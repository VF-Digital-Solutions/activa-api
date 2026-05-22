from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.assets.models import (
    Asset,
    AssetCategory,
    AssetDocument,
    AssetUsageLog,
    MaintenanceRecord,
)
from apps.assets.serializers import (
    AssetSerializer,
    AssetCategorySerializer,
    AssetDocumentSerializer,
    AssetUsageLogSerializer,
    MaintenanceRecordSerializer,
)


class AssetCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = AssetCategory.objects.filter(parent__isnull=True)
        serializer = AssetCategorySerializer(categories, many=True)
        return Response(serializer.data)


class AssetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

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


class AssetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk, is_active=True)
        except Asset.DoesNotExist:
            return None

    def get(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(AssetSerializer(asset).data)

    def patch(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AssetSerializer(asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        asset = self.get_object(pk)
        if not asset:
            return Response(status=status.HTTP_404_NOT_FOUND)
        asset.is_active = False
        asset.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssetDocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        documents = AssetDocument.objects.filter(asset_id=pk)
        serializer = AssetDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data.copy()
        data["asset"] = pk
        serializer = AssetDocumentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uploaded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssetUsageLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        logs = AssetUsageLog.objects.filter(asset_id=pk)
        serializer = AssetUsageLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data.copy()
        data["asset"] = pk
        serializer = AssetUsageLogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(recorded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MaintenanceRecordListCreateView(APIView):
    permission_classes = [IsAuthenticated]

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


class MaintenanceRecordDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MaintenanceRecord.objects.get(pk=pk)
        except MaintenanceRecord.DoesNotExist:
            return None

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
