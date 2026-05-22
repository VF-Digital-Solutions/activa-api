from django.urls import path
from apps.assets.views import (
    AssetCategoryListView,
    AssetListCreateView,
    AssetDetailView,
    AssetDocumentListCreateView,
    AssetUsageLogListCreateView,
    MaintenanceRecordListCreateView,
    MaintenanceRecordDetailView,
)

urlpatterns = [
    path("categories/", AssetCategoryListView.as_view(), name="asset-categories"),
    path("", AssetListCreateView.as_view(), name="asset-list-create"),
    path("<uuid:pk>/", AssetDetailView.as_view(), name="asset-detail"),
    path(
        "<uuid:pk>/documents/",
        AssetDocumentListCreateView.as_view(),
        name="asset-documents",
    ),
    path(
        "<uuid:pk>/usage-logs/",
        AssetUsageLogListCreateView.as_view(),
        name="asset-usage-logs",
    ),
    path(
        "<uuid:pk>/maintenance/",
        MaintenanceRecordListCreateView.as_view(),
        name="asset-maintenance",
    ),
    path(
        "maintenance/<uuid:pk>/",
        MaintenanceRecordDetailView.as_view(),
        name="maintenance-detail",
    ),
]
