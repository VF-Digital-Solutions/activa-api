from rest_framework import serializers

from apps.insight.models import IVISnapshot


class IVISnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = IVISnapshot
        fields = [
            "snapshot_date",
            "ivi",
            "assets",
            "liabilities",
            "adaptation",
            "assets_by_dimension",
        ]
        read_only_fields = fields


class IVITrendsQuerySerializer(serializers.Serializer):
    days = serializers.IntegerField(required=False, min_value=1, max_value=365, default=90)
