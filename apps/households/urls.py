from django.urls import path
from apps.households.views import (
    HouseholdListCreateView,
    HouseholdDetailView,
    HouseholdMemberListView,
    HouseholdInviteView,
)

urlpatterns = [
    path("", HouseholdListCreateView.as_view(), name="household-list-create"),
    path("<uuid:pk>/", HouseholdDetailView.as_view(), name="household-detail"),
    path(
        "<uuid:pk>/members/",
        HouseholdMemberListView.as_view(),
        name="household-members",
    ),
    path("<uuid:pk>/invite/", HouseholdInviteView.as_view(), name="household-invite"),
]
