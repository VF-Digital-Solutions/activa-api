from django.contrib import admin
from .models import (
    Card, CardBenefit, CardBenefitUsage,
    LoyaltyProgram, LoyaltyTransaction, LoyaltyRedemptionOption,
)


class CardBenefitInline(admin.TabularInline):
    model = CardBenefit
    extra = 0
    fields = ("title", "category", "discount_type", "discount_value", "valid_from", "valid_until", "is_recurring")


class LoyaltyRedemptionOptionInline(admin.TabularInline):
    model = LoyaltyRedemptionOption
    extra = 0
    fields = ("title", "category", "points_required", "estimated_value", "valid_until")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    inlines = [CardBenefitInline]
    list_display = ("name", "user", "issuer", "bank", "last_four_digits", "household_node")
    list_filter = ("issuer",)
    search_fields = ("name", "bank", "user__email", "last_four_digits")
    raw_id_fields = ("user", "household_node")


@admin.register(CardBenefit)
class CardBenefitAdmin(admin.ModelAdmin):
    list_display = ("title", "card", "category", "discount_type", "discount_value", "valid_from", "valid_until", "is_recurring")
    list_filter = ("category", "discount_type", "is_recurring")
    search_fields = ("title", "card__name", "applies_to")
    raw_id_fields = ("card",)
    date_hierarchy = "valid_until"


@admin.register(CardBenefitUsage)
class CardBenefitUsageAdmin(admin.ModelAdmin):
    list_display = ("benefit", "user", "used_at", "amount_saved")
    search_fields = ("benefit__title", "user__email")
    raw_id_fields = ("benefit", "user")
    date_hierarchy = "used_at"


@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    inlines = [LoyaltyRedemptionOptionInline]
    list_display = ("program_name", "company", "user", "category", "member_tier", "current_balance", "points_currency_name")
    list_filter = ("category",)
    search_fields = ("program_name", "company", "user__email", "member_id")
    raw_id_fields = ("user", "household_node")


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ("program", "type", "amount", "balance_after", "transaction_date", "source")
    list_filter = ("type",)
    search_fields = ("program__program_name", "description", "reference_code")
    raw_id_fields = ("program",)
    date_hierarchy = "transaction_date"


@admin.register(LoyaltyRedemptionOption)
class LoyaltyRedemptionOptionAdmin(admin.ModelAdmin):
    list_display = ("title", "program", "category", "points_required", "estimated_value", "valid_until")
    list_filter = ("category",)
    search_fields = ("title", "program__program_name")
    raw_id_fields = ("program",)
