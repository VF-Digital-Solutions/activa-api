from rest_framework import serializers
from apps.finances.models import (
    FinanceAccount,
    FinanceCategory,
    FinanceTransaction,
    FinanceBudget,
    FinanceBudgetExecution,
    RecurringExpense,
)


class FinanceAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceAccount
        fields = [
            "id",
            "household_node",
            "name",
            "type",
            "currency",
            "initial_balance",
            "current_balance",
            "institution",
            "is_shared",
            "color",
            "icon",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "current_balance", "created_at", "updated_at"]


class FinanceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceCategory
        fields = [
            "id",
            "household_node",
            "name",
            "type",
            "icon",
            "color",
            "parent",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class FinanceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceTransaction
        fields = [
            "id",
            "account",
            "household_node",
            "created_by",
            "type",
            "amount",
            "currency",
            "category",
            "description",
            "transaction_date",
            "is_recurring",
            "recurrence_config",
            "linked_asset",
            "linked_reservation",
            "tags",
            "receipt_url",
            "transfer_to_account",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class FinanceBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceBudget
        fields = [
            "id",
            "household_node",
            "name",
            "category",
            "amount",
            "currency",
            "period",
            "period_start",
            "period_end",
            "alert_threshold",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class FinanceBudgetExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceBudgetExecution
        fields = [
            "id",
            "budget",
            "period_start",
            "period_end",
            "budgeted_amount",
            "executed_amount",
            "execution_percentage",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "budgeted_amount",
            "executed_amount",
            "execution_percentage",
            "status",
            "created_at",
        ]


class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = [
            "id",
            "household_node",
            "name",
            "category",
            "amount",
            "currency",
            "billing_day",
            "frequency",
            "linked_benefit",
            "reminder_days_before",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
