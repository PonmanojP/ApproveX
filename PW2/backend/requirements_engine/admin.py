from django.contrib import admin
from .models import RequirementSet, RequirementVersion


@admin.register(RequirementSet)
class RequirementSetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request_type",
        "bonafide_type",
        "created_by",
        "created_at",
    )
    list_filter = ("request_type", "bonafide_type")
    readonly_fields = ("created_at",)


@admin.register(RequirementVersion)
class RequirementVersionAdmin(admin.ModelAdmin):
    list_display = (
        "requirement_set",
        "version",
        "created_by",
        "created_at",
    )
    list_filter = ("version",)
    readonly_fields = ("version", "created_at")
