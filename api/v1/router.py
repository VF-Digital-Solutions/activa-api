from django.urls import include, path
from apps.identity import urls as identity_urls

urlpatterns = [
    path("auth/", include(identity_urls)),
    path("households/", include("apps.households.urls")),
]
