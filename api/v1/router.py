from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.identity.urls")),
    path("assessment/", include("apps.assessment.urls")),
    # Note: path("agenda/", include("apps.agenda.urls")) will be added in a
    # follow-up issue once apps.agenda gets CRUD endpoints.
    # Disabled for Activa MVP (2026-07-23): routes for household-management
    # modules currently out of INSTALLED_APPS. See config/settings/base.py.
    # path("households/", include("apps.households.urls")),
    # path("assets/", include("apps.assets.urls")),
    # path("routines/", include("apps.routines.urls")),
    # path("reservations/", include("apps.reservations.urls")),
    # path("benefits/", include("apps.benefits.urls")),
    # path("finances/", include("apps.finances.urls")),
    # path("notifications/", include("apps.notifications.urls")),
    # path("agenda-legacy/", include("apps.agenda_legacy.urls")),  # renamed from apps.agenda
]
