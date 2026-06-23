from django.contrib import admin
from .models import (
    FinanceAccount, FinanceCategory, FinanceTransaction,
    FinanceBudget, FinanceBudgetExecution, RecurringExpense,
)


class FinanceBudgetExecutionInline(admin.TabularInline):
    model = FinanceBudgetExecution
    extra = 0
    readonly_fields = ("execution_percentage",)
    fields = ("period_start", "period_end", "budgeted_amount", "executed_amount", "execution_percentage", "status")


@admin.register(FinanceAccount)
class FinanceAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "household_node", "type", "currency", "current_balance", "is_shared")
    list_filter = ("type", "currency", "is_shared")
    search_fields = ("name", "institution", "household_node__name")
    raw_id_fields = ("household_node",)


@admin.register(FinanceCategory)
class FinanceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "parent", "household_node")
    list_filter = ("type",)
    search_fields = ("name",)
    raw_id_fields = ("household_node", "parent")


@admin.register(FinanceTransaction)
class FinanceTransactionAdmin(admin.ModelAdmin):
    list_display = ("type", "amount", "currency", "account", "household_node", "transaction_date", "category")
    list_filter = ("type", "currency", "is_recurring")
    search_fields = ("description", "account__name", "household_node__name")
    raw_id_fields = ("account", "household_node", "created_by", "category", "linked_asset", "linked_reservation", "transfer_to_account")
    date_hierarchy = "transaction_date"


@admin.register(FinanceBudget)
class FinanceBudgetAdmin(admin.ModelAdmin):
    inlines = [FinanceBudgetExecutionInline]
    list_display = ("name", "household_node", "amount", "currency", "period", "alert_threshold")
    list_filter = ("period", "currency")
    search_fields = ("name", "household_node__name")
    raw_id_fields = ("household_node", "category")


@admin.register(FinanceBudgetExecution)
class FinanceBudgetExecutionAdmin(admin.ModelAdmin):
    list_display = ("budget", "period_start", "period_end", "budgeted_amount", "executed_amount", "execution_percentage", "status")
    list_filter = ("status",)
    search_fields = ("budget__name",)
    raw_id_fields = ("budget",)
    readonly_fields = ("execution_percentage",)
    date_hierarchy = "period_start"


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ("name", "household_node", "amount", "currency", "frequency", "billing_day", "is_active")
    list_filter = ("frequency", "is_active", "currency")
    search_fields = ("name", "household_node__name")
    raw_id_fields = ("household_node", "category", "linked_benefit")
