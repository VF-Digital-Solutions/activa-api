from django.urls import path
from apps.finances.views import (
    FinanceAccountListCreateView,
    FinanceAccountDetailView,
    FinanceCategoryListCreateView,
    FinanceTransactionListCreateView,
    FinanceTransactionDetailView,
    FinanceBudgetListCreateView,
    FinanceBudgetDetailView,
    FinanceBudgetExecutionListView,
    RecurringExpenseListCreateView,
    RecurringExpenseDetailView,
)

urlpatterns = [
    # Accounts
    path(
        "accounts/",
        FinanceAccountListCreateView.as_view(),
        name="finance-account-list-create",
    ),
    path(
        "accounts/<uuid:pk>/",
        FinanceAccountDetailView.as_view(),
        name="finance-account-detail",
    ),
    # Categories
    path(
        "categories/",
        FinanceCategoryListCreateView.as_view(),
        name="finance-category-list-create",
    ),
    # Transactions
    path(
        "transactions/",
        FinanceTransactionListCreateView.as_view(),
        name="finance-transaction-list-create",
    ),
    path(
        "transactions/<uuid:pk>/",
        FinanceTransactionDetailView.as_view(),
        name="finance-transaction-detail",
    ),
    # Budgets
    path(
        "budgets/",
        FinanceBudgetListCreateView.as_view(),
        name="finance-budget-list-create",
    ),
    path(
        "budgets/<uuid:pk>/",
        FinanceBudgetDetailView.as_view(),
        name="finance-budget-detail",
    ),
    path(
        "budgets/<uuid:pk>/executions/",
        FinanceBudgetExecutionListView.as_view(),
        name="finance-budget-executions",
    ),
    # Recurring Expenses
    path(
        "recurring/",
        RecurringExpenseListCreateView.as_view(),
        name="finance-recurring-list-create",
    ),
    path(
        "recurring/<uuid:pk>/",
        RecurringExpenseDetailView.as_view(),
        name="finance-recurring-detail",
    ),
]
