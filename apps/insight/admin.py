from django.contrib import admin

from .models import IVISnapshot


@admin.register(IVISnapshot)
class IVISnapshotAdmin(admin.ModelAdmin):
    list_display = ("user", "snapshot_date", "ivi", "assets", "liabilities", "adaptation")
    search_fields = ("user__email",)
    raw_id_fields = ("user",)
    date_hierarchy = "snapshot_date"
