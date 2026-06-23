from django.contrib import admin
from .models import ReservationCategory, Reservation, ReservationReminder, ReservationDocument


class ReservationReminderInline(admin.TabularInline):
    model = ReservationReminder
    extra = 0
    fields = ("remind_at", "channels", "sent")


class ReservationDocumentInline(admin.TabularInline):
    model = ReservationDocument
    extra = 0
    fields = ("name", "type", "file_url")


@admin.register(ReservationCategory)
class ReservationCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = [ReservationReminderInline, ReservationDocumentInline]
    list_display = ("title", "user", "type", "status", "starts_at", "ends_at", "location_name")
    list_filter = ("type", "status", "is_all_day")
    search_fields = ("title", "user__email", "provider_name", "confirmation_code", "location_name")
    raw_id_fields = ("user", "household_node", "category", "linked_asset")
    date_hierarchy = "starts_at"


@admin.register(ReservationReminder)
class ReservationReminderAdmin(admin.ModelAdmin):
    list_display = ("reservation", "remind_at", "sent")
    list_filter = ("sent",)
    search_fields = ("reservation__title",)
    raw_id_fields = ("reservation",)


@admin.register(ReservationDocument)
class ReservationDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "reservation", "type")
    list_filter = ("type",)
    search_fields = ("name", "reservation__title")
    raw_id_fields = ("reservation",)
