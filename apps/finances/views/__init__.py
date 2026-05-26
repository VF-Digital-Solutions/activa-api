from django.db import models as db_models
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.finances.models import (
    FinanceAccount,
    FinanceCategory,
    FinanceTransaction,
    FinanceBudget,
    FinanceBudgetExecution,
    RecurringExpense,
)
from apps.finances.serializers import (
    FinanceAccountSerializer,
    FinanceCategorySerializer,
    FinanceTransactionSerializer,
    FinanceBudgetSerializer,
    FinanceBudgetExecutionSerializer,
    RecurringExpenseSerializer,
)


@extend_schema(tags=["Finances - Accounts"])
class FinanceAccountListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List finance accounts",
        description="Returns all active finance accounts for a household.",
        responses={200: FinanceAccountSerializer(many=True)},
    )
    def get(self, request):
        household_id = request.query_params.get("household")
        accounts = FinanceAccount.objects.filter(is_active=True)
        if household_id:
            accounts = accounts.filter(household_node_id=household_id)
        serializer = FinanceAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create finance account",
        description="Creates a new finance account for a household.",
        request=FinanceAccountSerializer,
        responses={201: FinanceAccountSerializer},
    )
    def post(self, request):
        serializer = FinanceAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        account.current_balance = account.initial_balance
        account.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Finances - Accounts"])
class FinanceAccountDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FinanceAccount.objects.get(pk=pk, is_active=True)
        except FinanceAccount.DoesNotExist:
            return None

    @extend_schema(
        summary="Get finance account",
        description="Returns a finance account by ID.",
        responses={200: FinanceAccountSerializer},
    )
    def get(self, request, pk):
        account = self.get_object(pk)
        if not account:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(FinanceAccountSerializer(account).data)

    @extend_schema(
        summary="Update finance account",
        description="Partially updates a finance account.",
        request=FinanceAccountSerializer,
        responses={200: FinanceAccountSerializer},
    )
    def patch(self, request, pk):
        account = self.get_object(pk)
        if not account:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FinanceAccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete finance account",
        description="Soft deletes a finance account.",
        responses={204: None},
    )
    def delete(self, request, pk):
        account = self.get_object(pk)
        if not account:
            return Response(status=status.HTTP_404_NOT_FOUND)
        account.is_active = False
        account.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Finances - Categories"])
class FinanceCategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List finance categories",
        description="Returns all finance categories.",
        responses={200: FinanceCategorySerializer(many=True)},
    )
    def get(self, request):
        categories = FinanceCategory.objects.filter(parent__isnull=True)
        serializer = FinanceCategorySerializer(categories, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create finance category",
        description="Creates a new finance category.",
        request=FinanceCategorySerializer,
        responses={201: FinanceCategorySerializer},
    )
    def post(self, request):
        serializer = FinanceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Finances - Transactions"])
class FinanceTransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List transactions",
        description="Returns all transactions. Filter by account using ?account=<id>.",
        responses={200: FinanceTransactionSerializer(many=True)},
    )
    def get(self, request):
        account_id = request.query_params.get("account")
        transactions = FinanceTransaction.objects.all()
        if account_id:
            transactions = transactions.filter(account_id=account_id)
        serializer = FinanceTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create transaction",
        description="Creates a new financial transaction and updates account balance.",
        request=FinanceTransactionSerializer,
        responses={201: FinanceTransactionSerializer},
    )
    def post(self, request):
        serializer = FinanceTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(created_by=request.user)

        account = transaction.account
        if transaction.type == FinanceTransaction.Type.INCOME:
            account.current_balance += transaction.amount
        elif transaction.type == FinanceTransaction.Type.EXPENSE:
            account.current_balance -= transaction.amount
        elif transaction.type == FinanceTransaction.Type.TRANSFER:
            account.current_balance -= transaction.amount
            if transaction.transfer_to_account:
                transaction.transfer_to_account.current_balance += transaction.amount
                transaction.transfer_to_account.save()
        account.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Finances - Transactions"])
class FinanceTransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FinanceTransaction.objects.get(pk=pk)
        except FinanceTransaction.DoesNotExist:
            return None

    @extend_schema(
        summary="Get transaction",
        description="Returns a transaction by ID.",
        responses={200: FinanceTransactionSerializer},
    )
    def get(self, request, pk):
        transaction = self.get_object(pk)
        if not transaction:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(FinanceTransactionSerializer(transaction).data)

    @extend_schema(
        summary="Delete transaction",
        description="Deletes a transaction.",
        responses={204: None},
    )
    def delete(self, request, pk):
        transaction = self.get_object(pk)
        if not transaction:
            return Response(status=status.HTTP_404_NOT_FOUND)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Finances - Budgets"])
class FinanceBudgetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List budgets",
        description="Returns all budgets for a household.",
        responses={200: FinanceBudgetSerializer(many=True)},
    )
    def get(self, request):
        household_id = request.query_params.get("household")
        budgets = FinanceBudget.objects.all()
        if household_id:
            budgets = budgets.filter(household_node_id=household_id)
        serializer = FinanceBudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create budget",
        description="Creates a new budget for a household.",
        request=FinanceBudgetSerializer,
        responses={201: FinanceBudgetSerializer},
    )
    def post(self, request):
        serializer = FinanceBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Finances - Budgets"])
class FinanceBudgetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FinanceBudget.objects.get(pk=pk)
        except FinanceBudget.DoesNotExist:
            return None

    @extend_schema(
        summary="Get budget",
        description="Returns a budget by ID.",
        responses={200: FinanceBudgetSerializer},
    )
    def get(self, request, pk):
        budget = self.get_object(pk)
        if not budget:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(FinanceBudgetSerializer(budget).data)

    @extend_schema(
        summary="Update budget",
        description="Partially updates a budget.",
        request=FinanceBudgetSerializer,
        responses={200: FinanceBudgetSerializer},
    )
    def patch(self, request, pk):
        budget = self.get_object(pk)
        if not budget:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FinanceBudgetSerializer(budget, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete budget",
        description="Deletes a budget.",
        responses={204: None},
    )
    def delete(self, request, pk):
        budget = self.get_object(pk)
        if not budget:
            return Response(status=status.HTTP_404_NOT_FOUND)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Finances - Budgets"])
class FinanceBudgetExecutionListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List budget executions",
        description="Returns all execution records for a budget.",
        responses={200: FinanceBudgetExecutionSerializer(many=True)},
    )
    def get(self, request, pk):
        executions = FinanceBudgetExecution.objects.filter(budget_id=pk)
        serializer = FinanceBudgetExecutionSerializer(executions, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Finances - Recurring"])
class RecurringExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List recurring expenses",
        description="Returns all recurring expenses for a household.",
        responses={200: RecurringExpenseSerializer(many=True)},
    )
    def get(self, request):
        household_id = request.query_params.get("household")
        expenses = RecurringExpense.objects.filter(is_active=True)
        if household_id:
            expenses = expenses.filter(household_node_id=household_id)
        serializer = RecurringExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create recurring expense",
        description="Creates a new recurring expense for a household.",
        request=RecurringExpenseSerializer,
        responses={201: RecurringExpenseSerializer},
    )
    def post(self, request):
        serializer = RecurringExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Finances - Recurring"])
class RecurringExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RecurringExpense.objects.get(pk=pk)
        except RecurringExpense.DoesNotExist:
            return None

    @extend_schema(
        summary="Get recurring expense",
        description="Returns a recurring expense by ID.",
        responses={200: RecurringExpenseSerializer},
    )
    def get(self, request, pk):
        expense = self.get_object(pk)
        if not expense:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(RecurringExpenseSerializer(expense).data)

    @extend_schema(
        summary="Update recurring expense",
        description="Partially updates a recurring expense.",
        request=RecurringExpenseSerializer,
        responses={200: RecurringExpenseSerializer},
    )
    def patch(self, request, pk):
        expense = self.get_object(pk)
        if not expense:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RecurringExpenseSerializer(expense, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete recurring expense",
        description="Deletes a recurring expense.",
        responses={204: None},
    )
    def delete(self, request, pk):
        expense = self.get_object(pk)
        if not expense:
            return Response(status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

