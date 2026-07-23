from django.urls import path

from apps.capitals.views import EmotionalLogDetailView, EmotionalLogListCreateView

urlpatterns = [
    path(
        "emotional-logs/",
        EmotionalLogListCreateView.as_view(),
        name="emotional-log-list-create",
    ),
    path(
        "emotional-logs/<uuid:pk>/",
        EmotionalLogDetailView.as_view(),
        name="emotional-log-detail",
    ),
]
