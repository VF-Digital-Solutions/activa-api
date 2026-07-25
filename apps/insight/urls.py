from django.urls import path

from apps.insight.views import IVITrendsView

urlpatterns = [
    path("ivi/trends/", IVITrendsView.as_view(), name="ivi-trends"),
]
