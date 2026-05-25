from django.db import models
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.identity.models import User
from apps.households.models import HouseholdNode


class Card(SoftDeleteModel):

    class Issuer(models.TextChoices):
        VISA       = "VISA",       "Visa"
        MASTERCARD = "MASTERCARD", "Mastercard"
        AMEX       = "AMEX",       "American Express"
        OTHER      = "OTHER",      "Otro"

    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    household_node   = models.ForeignKey(HouseholdNode, on_delete=models.SET_NULL, null=True, blank=True, related_name="cards")
    name             = models.CharField(max_length=150)
    issuer           = models.CharField(max_length=15, choices=Issuer.choices, default=Issuer.OTHER)
    bank             = models.CharField(max_length=100, blank=True)
    last_four_digits = models.CharField(max_length=4, blank=True)
    color            = models.CharField(max_length=10, blank=True)
    icon             = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table     = "benefits_card"
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"

    def __str__(self):
        return f"{self.name} — {self.user.email}"


class CardBenefit(TimeStampedModel):

    class Category(models.TextChoices):
        CASHBACK      = "CASHBACK",      "Cashback"
        DISCOUNT      = "DISCOUNT",      "Descuento"
        FREE_SHIPPING = "FREE_SHIPPING", "Envío gratis"
        LOUNGE        = "LOUNGE",        "Sala VIP"
        OTHER         = "OTHER",         "Otro"

    class DiscountType(models.TextChoices):
        PERCENTAGE  = "PERCENTAGE",  "Porcentaje"
        FIXED       = "FIXED",       "Monto fijo"
        TWO_FOR_ONE = "TWO_FOR_ONE", "2x1"
        OTHER       = "OTHER",       "Otro"

    card            = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="benefits")
    title           = models.CharField(max_length=150)
    description     = models.TextField(blank=True)
    category        = models.CharField(max_length=15, choices=Category.choices, default=Category.OTHER)
    discount_type   = models.CharField(max_length=15, choices=DiscountType.choices, default=DiscountType.OTHER)
    discount_value  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    applies_to      = models.CharField(max_length=150, blank=True)
    conditions      = models.JSONField(default=dict, blank=True)
    valid_from      = models.DateField(null=True, blank=True)
    valid_until     = models.DateField(null=True, blank=True)
    is_recurring    = models.BooleanField(default=False)
    source_url      = models.URLField(blank=True, null=True)

    class Meta:
        db_table     = "benefits_card_benefit"
        verbose_name = "Beneficio de tarjeta"
        verbose_name_plural = "Beneficios de tarjetas"

    def __str__(self):
        return f"{self.title} — {self.card.name}"


class CardBenefitUsage(TimeStampedModel):
    benefit      = models.ForeignKey(CardBenefit, on_delete=models.CASCADE, related_name="usages")
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="benefit_usages")
    used_at      = models.DateField()
    amount_saved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes        = models.TextField(blank=True)

    class Meta:
        db_table     = "benefits_card_benefit_usage"
        verbose_name = "Uso de beneficio"
        verbose_name_plural = "Usos de beneficios"

    def __str__(self):
        return f"{self.benefit.title} — {self.used_at}"


class LoyaltyProgram(SoftDeleteModel):

    class Category(models.TextChoices):
        AIRLINE = "AIRLINE", "Aerolínea"
        HOTEL   = "HOTEL",   "Hotel"
        RETAIL  = "RETAIL",  "Retail"
        BANK    = "BANK",    "Banco"
        OTHER   = "OTHER",   "Otro"

    user                 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loyalty_programs")
    household_node       = models.ForeignKey(HouseholdNode, on_delete=models.SET_NULL, null=True, blank=True, related_name="loyalty_programs")
    program_name         = models.CharField(max_length=150)
    company              = models.CharField(max_length=100)
    category             = models.CharField(max_length=10, choices=Category.choices, default=Category.OTHER)
    member_id            = models.CharField(max_length=100, blank=True)
    member_tier          = models.CharField(max_length=50, blank=True)
    points_currency_name = models.CharField(max_length=50, default="puntos")
    current_balance      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_updated_at   = models.DateTimeField(null=True, blank=True)
    expiry_policy        = models.JSONField(default=dict, blank=True)
    notes                = models.TextField(blank=True)

    class Meta:
        db_table     = "benefits_loyalty_program"
        verbose_name = "Programa de fidelidad"
        verbose_name_plural = "Programas de fidelidad"

    def __str__(self):
        return f"{self.program_name} — {self.user.email}"


class LoyaltyTransaction(TimeStampedModel):

    class Type(models.TextChoices):
        EARNED      = "EARNED",      "Acumulado"
        REDEEMED    = "REDEEMED",    "Canjeado"
        EXPIRED     = "EXPIRED",     "Vencido"
        ADJUSTED    = "ADJUSTED",    "Ajustado"
        TRANSFERRED = "TRANSFERRED", "Transferido"

    program          = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="transactions")
    type             = models.CharField(max_length=15, choices=Type.choices)
    amount           = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after    = models.DecimalField(max_digits=12, decimal_places=2)
    description      = models.CharField(max_length=200, blank=True)
    transaction_date = models.DateField()
    source           = models.CharField(max_length=150, blank=True)
    reference_code   = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table     = "benefits_loyalty_transaction"
        verbose_name = "Transacción de fidelidad"
        verbose_name_plural = "Transacciones de fidelidad"
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{self.program.program_name} — {self.type}: {self.amount}"


class LoyaltyRedemptionOption(TimeStampedModel):

    class Category(models.TextChoices):
        FLIGHT   = "FLIGHT",   "Vuelo"
        HOTEL    = "HOTEL",    "Hotel"
        PRODUCT  = "PRODUCT",  "Producto"
        CASHBACK = "CASHBACK", "Cashback"
        OTHER    = "OTHER",    "Otro"

    program          = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="redemption_options")
    title            = models.CharField(max_length=150)
    description      = models.TextField(blank=True)
    points_required  = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_value  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category         = models.CharField(max_length=10, choices=Category.choices, default=Category.OTHER)
    valid_until      = models.DateField(null=True, blank=True)
    source_url       = models.URLField(blank=True, null=True)

    class Meta:
        db_table     = "benefits_loyalty_redemption_option"
        verbose_name = "Opción de canje"
        verbose_name_plural = "Opciones de canje"

    def __str__(self):
        return f"{self.title} — {self.points_required} {self.program.points_currency_name}"

