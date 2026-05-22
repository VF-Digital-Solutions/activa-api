from rest_framework import serializers
from apps.households.models import (
    HouseholdNode,
    HouseholdMembership,
    HouseholdInvitation,
)
from apps.identity.serializers import UserSerializer


class HouseholdNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdNode
        fields = [
            "id",
            "name",
            "description",
            "type",
            "parent",
            "avatar_url",
            "address",
            "settings",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class HouseholdMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = HouseholdMembership
        fields = [
            "id",
            "user",
            "node",
            "role",
            "nickname",
            "joined_at",
            "left_at",
        ]
        read_only_fields = ["id", "joined_at"]


class HouseholdInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseholdInvitation
        fields = [
            "id",
            "node",
            "invited_email",
            "role",
            "token",
            "status",
            "expires_at",
            "created_at",
        ]
        read_only_fields = ["id", "token", "status", "created_at"]
