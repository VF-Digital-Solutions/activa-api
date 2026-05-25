from rest_framework import serializers
from apps.benefits.models import (
    Card,
    CardBenefit,
    CardBenefitUsage,
    LoyaltyProgram,
    LoyaltyTransaction,
    LoyaltyRedemptionOption,
)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "user",
            "household_node",
            "name",
            "issuer",
            "bank",
            "last_four_digits",
            "color",
            "icon",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CardBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardBenefit
        fields = [
            "id",
            "card",
            "title",
            "description",
            "category",
            "discount_type",
            "discount_value",
            "applies_to",
            "conditions",
            "valid_from",
            "valid_until",
            "is_recurring",
            "source_url",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class CardBenefitUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardBenefitUsage
        fields = [
            "id",
            "benefit",
            "user",
            "used_at",
            "amount_saved",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]


class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = [
            "id",
            "user",
            "household_node",
            "program_name",
            "company",
            "category",
            "member_id",
            "member_tier",
            "points_currency_name",
            "current_balance",
            "balance_updated_at",
            "expiry_policy",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTransaction
        fields = [
            "id",
            "program",
            "type",
            "amount",
            "balance_after",
            "description",
            "transaction_date",
            "source",
            "reference_code",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class LoyaltyRedemptionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyRedemptionOption
        fields = [
            "id",
            "program",
            "title",
            "description",
            "points_required",
            "estimated_value",
            "category",
            "valid_until",
            "source_url",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
