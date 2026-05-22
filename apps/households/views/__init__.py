import uuid
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.households.models import (
    HouseholdNode,
    HouseholdMembership,
    HouseholdInvitation,
)
from apps.households.serializers import (
    HouseholdNodeSerializer,
    HouseholdMembershipSerializer,
    HouseholdInvitationSerializer,
)


class HouseholdListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        memberships = HouseholdMembership.objects.filter(
            user=request.user, left_at__isnull=True
        ).select_related("node")
        nodes = [m.node for m in memberships]
        serializer = HouseholdNodeSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HouseholdNodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node = serializer.save()
        HouseholdMembership.objects.create(
            user=request.user,
            node=node,
            role=HouseholdMembership.Role.OWNER,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HouseholdDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            node = HouseholdNode.objects.get(pk=pk, is_active=True)
            HouseholdMembership.objects.get(user=user, node=node, left_at__isnull=True)
            return node
        except (HouseholdNode.DoesNotExist, HouseholdMembership.DoesNotExist):
            return None

    def get(self, request, pk):
        node = self.get_object(pk, request.user)
        if not node:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(HouseholdNodeSerializer(node).data)

    def patch(self, request, pk):
        node = self.get_object(pk, request.user)
        if not node:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HouseholdNodeSerializer(node, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        node = self.get_object(pk, request.user)
        if not node:
            return Response(status=status.HTTP_404_NOT_FOUND)
        node.is_active = False
        node.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HouseholdMemberListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        memberships = HouseholdMembership.objects.filter(
            node_id=pk, left_at__isnull=True
        ).select_related("user")
        serializer = HouseholdMembershipSerializer(memberships, many=True)
        return Response(serializer.data)


class HouseholdInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            node = HouseholdNode.objects.get(pk=pk, is_active=True)
            membership = HouseholdMembership.objects.get(
                user=request.user, node=node, left_at__isnull=True
            )
        except (HouseholdNode.DoesNotExist, HouseholdMembership.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if membership.role not in [
            HouseholdMembership.Role.OWNER,
            HouseholdMembership.Role.ADMIN,
        ]:
            return Response(
                {"detail": "No tenés permisos para invitar miembros."},
                status=status.HTTP_403_FORBIDDEN,
            )

        invitation = HouseholdInvitation.objects.create(
            node=node,
            invited_email=request.data.get("email"),
            invited_by=request.user,
            role=request.data.get("role", HouseholdMembership.Role.MEMBER),
            token=uuid.uuid4(),
            expires_at=timezone.now() + timedelta(days=7),
        )
        return Response(
            HouseholdInvitationSerializer(invitation).data,
            status=status.HTTP_201_CREATED,
        )
