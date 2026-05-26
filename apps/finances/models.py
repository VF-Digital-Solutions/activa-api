from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.identity.models import User
from apps.households.models import HouseholdNode
from apps.assets.models import Asset
from apps.benefits.models import CardBenefit


class FinanceAccount(SoftDeleteModel):

    class Type(models.TextChoices):
        CASH       = "CASH",       "Efectivo"
        BANK       = "BANK",       "Cuenta bancaria"
        SAVINGS    = "SAVINGS",    "Ahorros"
        INVESTMENT = "INVESTMENT", "Inversión"
        CREDIT     = "CREDIT",     "Crédito"
        OTHER      = "OTHER",      "Otro"

    household_node  = models.ForeignKey(HouseholdNode, on_delete=models.CASCADE, related_name="finance_accounts")
    name            = models.CharField(max_length=150)
    type            = models.CharField(max_length=15, choices=Type.choices, default=Type.BANK)
    currency        = models.CharField(max_length=10, default="USD")
    initial_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    institution     = models.CharField(max_length=100, blank=True)
    is_shared       = models.BooleanField(default=False)
    color           = models.CharField(max_length=10, blank=True)
    icon            = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table     = "finances_account"
        verbose_name = "Cuenta financiera"
        verbose_name_plural = "Cuentas financieras"

    def __str__(self):
        return f"{self.name} — {self.household_node.name}"


class FinanceCategory(TimeStampedModel):

    class Type(models.TextChoices):
        INCOME  = "INCOME",  "Ingreso"
        EXPENSE = "EXPENSE", "Gasto"

    household_node = models.ForeignKey(HouseholdNode, on_delete=models.SET_NULL, null=True, blank=True, related_name="finance_categories")
    name           = models.CharField(max_length=100)
    type           = models.CharField(max_length=10, choices=Type.choices)
    icon           = models.CharField(max_length=50, blank=True)
    color          = models.CharField(max_length=10, blank=True)
    parent         = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    class Meta:
        db_table     = "finances_category"
        verbose_name = "Categoría financiera"
        verbose_name_plural = "Categorías financieras"

    def __str__(self):
        return f"{self.name} ({self.type})"


class FinanceTransaction(TimeStampedModel):

    class Type(models.TextChoices):
        INCOME   = "INCOME",   "Ingreso"
        EXPENSE  = "EXPENSE",  "Gasto"
        TRANSFER = "TRANSFER", "Transferencia"

    account              = models.ForeignKey(FinanceAccount, on_delete=models.CASCADE, related_name="transactions")
    household_node       = models.ForeignKey(HouseholdNode, on_delete=models.CASCADE, related_name="transactions")
    created_by           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type                 = models.CharField(max_length=10, choices=Type.choices)
    amount               = models.DecimalField(max_digits=14, decimal_places=2)
    currency             = models.CharField(max_length=10, default="USD")
    category             = models.ForeignKey(FinanceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description          = models.CharField(max_length=200, blank=True)
    transaction_date     = models.DateField()
    is_recurring         = models.BooleanField(default=False)
    recurrence_config    = models.JSONField(default=dict, blank=True)
    linked_asset         = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    linked_reservation   = models.ForeignKey("reservations.Reservation", on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    tags                 = models.JSONField(default=list, blank=True)
    receipt_url          = models.URLField(blank=True, null=True)
    transfer_to_account  = models.ForeignKey(FinanceAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name="incoming_transfers")

    class Meta:
        db_table     = "finances_transaction"
        verbose_name = "Transacción financiera"
        verbose_name_plural = "Transacciones financieras"
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{self.type}: {self.amount} {self.currency} — {self.transaction_date}"


class FinanceBudget(TimeStampedModel):

    class Period(models.TextChoices):
        MONTHLY   = "MONTHLY",   "Mensual"
        QUARTERLY = "QUARTERLY", "Trimestral"
        ANNUAL    = "ANNUAL",    "Anual"
        CUSTOM    = "CUSTOM",    "Personalizado"

    household_node  = models.ForeignKey(HouseholdNode, on_delete=models.CASCADE, related_name="budgets")
    name            = models.CharField(max_length=150)
    category        = models.ForeignKey(FinanceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    amount          = models.DecimalField(max_digits=14, decimal_places=2)
    currency        = models.CharField(max_length=10, default="USD")
    period          = models.CharField(max_length=10, choices=Period.choices, default=Period.MONTHLY)
    period_start    = models.DateField(null=True, blank=True)
    period_end      = models.DateField(null=True, blank=True)
    alert_threshold = models.PositiveIntegerField(default=80)

    class Meta:
        db_table     = "finances_budget"
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return f"{self.name} — {self.amount} {self.currency}"


class FinanceBudgetExecution(TimeStampedModel):

    class Status(models.TextChoices):
        ON_TRACK  = "ON_TRACK",  "En curso"
        WARNING   = "WARNING",   "Alerta"
        EXCEEDED  = "EXCEEDED",  "Excedido"

    budget             = models.ForeignKey(FinanceBudget, on_delete=models.CASCADE, related_name="executions")
    period_start       = models.DateField()
    period_end         = models.DateField()
    budgeted_amount    = models.DecimalField(max_digits=14, decimal_places=2)
    executed_amount    = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    execution_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status             = models.CharField(max_length=10, choices=Status.choices, default=Status.ON_TRACK)

    class Meta:
        db_table     = "finances_budget_execution"
        verbose_name = "Ejecución de presupuesto"
        verbose_name_plural = "Ejecuciones de presupuesto"

    def __str__(self):
        return f"{self.budget.name} — {self.period_start} ({self.status})"


class RecurringExpense(TimeStampedModel):

    class Frequency(models.TextChoices):
        MONTHLY = "MONTHLY", "Mensual"
        ANNUAL  = "ANNUAL",  "Anual"
        WEEKLY  = "WEEKLY",  "Semanal"
        OTHER   = "OTHER",   "Otro"

    household_node       = models.ForeignKey(HouseholdNode, on_delete=models.CASCADE, related_name="recurring_expenses")
    name                 = models.CharField(max_length=150)
    category             = models.ForeignKey(FinanceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    amount               = models.DecimalField(max_digits=14, decimal_places=2)
    currency             = models.CharField(max_length=10, default="USD")
    billing_day          = models.PositiveIntegerField()
    frequency            = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.MONTHLY)
    linked_benefit       = models.ForeignKey(CardBenefit, on_delete=models.SET_NULL, null=True, blank=True, related_name="recurring_expenses")
    reminder_days_before = models.PositiveIntegerField(default=3)
    is_active            = models.BooleanField(default=True)

    class Meta:
        db_table     = "finances_recurring_expense"
        verbose_name = "Gasto recurrente"
        verbose_name_plural = "Gastos recurrentes"

    def __str__(self):
        return f"{self.name} — {self.amount} {self.currency}"

