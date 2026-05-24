from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.identity.urls")),
    path("households/", include("apps.households.urls")),
    path("assets/", include("apps.assets.urls")),
    path("routines/", include("apps.routines.urls")),
    path("reservations/", include("apps.reservations.urls")),
]
