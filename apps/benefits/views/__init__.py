from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.benefits.models import (
    Card,
    CardBenefit,
    CardBenefitUsage,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyRedemptionOption,
)
from apps.benefits.serializers import (
    CardSerializer,
    CardBenefitSerializer,
    CardBenefitUsageSerializer,
    LoyaltyProgramSerializer,
    LoyaltyTransactionSerializer,
    LoyaltyRedemptionOptionSerializer,
)


@extend_schema(tags=["Benefits - Cards"])
class CardListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List cards",
        description="Returns all active cards for the authenticated user.",
        responses={200: CardSerializer(many=True)},
    )
    def get(self, request):
        cards = Card.objects.filter(user=request.user, is_active=True)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create card",
        description="Creates a new card for the authenticated user.",
        request=CardSerializer,
        responses={201: CardSerializer},
    )
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Benefits - Cards"])
class CardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Card.objects.get(pk=pk, user=user, is_active=True)
        except Card.DoesNotExist:
            return None

    @extend_schema(
        summary="Get card",
        description="Returns a card by ID.",
        responses={200: CardSerializer},
    )
    def get(self, request, pk):
        card = self.get_object(pk, request.user)
        if not card:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(CardSerializer(card).data)

    @extend_schema(
        summary="Update card",
        description="Partially updates a card.",
        request=CardSerializer,
        responses={200: CardSerializer},
    )
    def patch(self, request, pk):
        card = self.get_object(pk, request.user)
        if not card:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CardSerializer(card, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete card",
        description="Soft deletes a card.",
        responses={204: None},
    )
    def delete(self, request, pk):
        card = self.get_object(pk, request.user)
        if not card:
            return Response(status=status.HTTP_404_NOT_FOUND)
        card.is_active = False
        card.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Benefits - Cards"])
class CardBenefitListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List card benefits",
        description="Returns all benefits for a card.",
        responses={200: CardBenefitSerializer(many=True)},
    )
    def get(self, request, pk):
        benefits = CardBenefit.objects.filter(card_id=pk)
        serializer = CardBenefitSerializer(benefits, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create card benefit",
        description="Creates a new benefit for a card.",
        request=CardBenefitSerializer,
        responses={201: CardBenefitSerializer},
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["card"] = pk
        serializer = CardBenefitSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Benefits - Cards"])
class CardBenefitUsageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Register benefit usage",
        description="Records a usage of a card benefit.",
        request=CardBenefitUsageSerializer,
        responses={201: CardBenefitUsageSerializer},
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["benefit"] = pk
        serializer = CardBenefitUsageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Benefits - Loyalty"])
class LoyaltyProgramListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List loyalty programs",
        description="Returns all active loyalty programs for the authenticated user.",
        responses={200: LoyaltyProgramSerializer(many=True)},
    )
    def get(self, request):
        programs = LoyaltyProgram.objects.filter(user=request.user, is_active=True)
        serializer = LoyaltyProgramSerializer(programs, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create loyalty program",
        description="Creates a new loyalty program for the authenticated user.",
        request=LoyaltyProgramSerializer,
        responses={201: LoyaltyProgramSerializer},
    )
    def post(self, request):
        serializer = LoyaltyProgramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Benefits - Loyalty"])
class LoyaltyProgramDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return LoyaltyProgram.objects.get(pk=pk, user=user, is_active=True)
        except LoyaltyProgram.DoesNotExist:
            return None

    @extend_schema(
        summary="Get loyalty program",
        description="Returns a loyalty program by ID.",
        responses={200: LoyaltyProgramSerializer},
    )
    def get(self, request, pk):
        program = self.get_object(pk, request.user)
        if not program:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(LoyaltyProgramSerializer(program).data)

    @extend_schema(
        summary="Update loyalty program",
        description="Partially updates a loyalty program.",
        request=LoyaltyProgramSerializer,
        responses={200: LoyaltyProgramSerializer},
    )
    def patch(self, request, pk):
        program = self.get_object(pk, request.user)
        if not program:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoyaltyProgramSerializer(program, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete loyalty program",
        description="Soft deletes a loyalty program.",
        responses={204: None},
    )
    def delete(self, request, pk):
        program = self.get_object(pk, request.user)
        if not program:
            return Response(status=status.HTTP_404_NOT_FOUND)
        program.is_active = False
        program.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Benefits - Loyalty"])
class LoyaltyTransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List loyalty transactions",
        description="Returns all transactions for a loyalty program.",
        responses={200: LoyaltyTransactionSerializer(many=True)},
    )
    def get(self, request, pk):
        transactions = LoyaltyTransaction.objects.filter(program_id=pk)
        serializer = LoyaltyTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create loyalty transaction",
        description="Records a new transaction for a loyalty program.",
        request=LoyaltyTransactionSerializer,
        responses={201: LoyaltyTransactionSerializer},
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["program"] = pk
        serializer = LoyaltyTransactionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Benefits - Loyalty"])
class LoyaltyRedemptionOptionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List redemption options",
        description="Returns all redemption options for a loyalty program.",
        responses={200: LoyaltyRedemptionOptionSerializer(many=True)},
    )
    def get(self, request, pk):
        options = LoyaltyRedemptionOption.objects.filter(program_id=pk)
        serializer = LoyaltyRedemptionOptionSerializer(options, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create redemption option",
        description="Creates a new redemption option for a loyalty program.",
        request=LoyaltyRedemptionOptionSerializer,
        responses={201: LoyaltyRedemptionOptionSerializer},
    )
    def post(self, request, pk):
        data = request.data.copy()
        data["program"] = pk
        serializer = LoyaltyRedemptionOptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

