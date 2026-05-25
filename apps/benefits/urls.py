from django.urls import path
from apps.benefits.views import (
    CardListCreateView,
    CardDetailView,
    CardBenefitListCreateView,
    CardBenefitUsageCreateView,
    LoyaltyProgramListCreateView,
    LoyaltyProgramDetailView,
    LoyaltyTransactionListCreateView,
    LoyaltyRedemptionOptionListCreateView,
)

urlpatterns = [
    # Cards
    path("cards/", CardListCreateView.as_view(), name="card-list-create"),
    path("cards/<uuid:pk>/", CardDetailView.as_view(), name="card-detail"),
    path(
        "cards/<uuid:pk>/benefits/",
        CardBenefitListCreateView.as_view(),
        name="card-benefits",
    ),
    path(
        "benefits/<uuid:pk>/usage/",
        CardBenefitUsageCreateView.as_view(),
        name="benefit-usage",
    ),
    # Loyalty Programs
    path(
        "loyalty/", LoyaltyProgramListCreateView.as_view(), name="loyalty-list-create"
    ),
    path(
        "loyalty/<uuid:pk>/", LoyaltyProgramDetailView.as_view(), name="loyalty-detail"
    ),
    path(
        "loyalty/<uuid:pk>/transactions/",
        LoyaltyTransactionListCreateView.as_view(),
        name="loyalty-transactions",
    ),
    path(
        "loyalty/<uuid:pk>/redemptions/",
        LoyaltyRedemptionOptionListCreateView.as_view(),
        name="loyalty-redemptions",
    ),
]
