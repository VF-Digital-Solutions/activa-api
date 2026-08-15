from django.urls import path

from apps.health.views import SleepLogDetailView, SleepLogListCreateView

urlpatterns = [
    path("sleep-logs/", SleepLogListCreateView.as_view(), name="sleep-log-list-create"),
    path("sleep-logs/<uuid:pk>/", SleepLogDetailView.as_view(), name="sleep-log-detail"),
]
