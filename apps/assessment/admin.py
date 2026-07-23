from django.contrib import admin

from .models import (
    Assessment,
    AssessmentAttempt,
    AssessmentResponse,
    AssessmentSnapshot,
    Question,
)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("order", "text", "capital_dimension", "scale_type")
    ordering = ("order",)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "type", "version")
    list_filter = ("type",)
    search_fields = ("title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("assessment", "order", "capital_dimension", "scale_type")
    list_filter = ("capital_dimension", "scale_type", "assessment")
    search_fields = ("text",)
    raw_id_fields = ("assessment",)


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "assessment", "status", "created_at", "completed_at")
    list_filter = ("status", "assessment")
    search_fields = ("user__email",)
    raw_id_fields = ("user", "assessment")
    date_hierarchy = "created_at"


@admin.register(AssessmentResponse)
class AssessmentResponseAdmin(admin.ModelAdmin):
    list_display = ("user", "assessment", "question", "score", "created_at")
    list_filter = ("assessment",)
    search_fields = ("user__email",)
    raw_id_fields = ("attempt", "user", "assessment", "question")
    date_hierarchy = "created_at"


@admin.register(AssessmentSnapshot)
class AssessmentSnapshotAdmin(admin.ModelAdmin):
    list_display = ("user", "assessment", "snapshot_date")
    list_filter = ("assessment",)
    search_fields = ("user__email",)
    raw_id_fields = ("attempt", "user", "assessment")
    date_hierarchy = "snapshot_date"
