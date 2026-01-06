from django.contrib import admin
from .models import AuditEvent, AIExplanation


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "actor",
        "action",
        "created_at",
    )
    list_filter = ("action",)
    search_fields = ("actor__username",)
    readonly_fields = ("created_at",)


@admin.register(AIExplanation)
class AIExplanationAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "explanation_type",
        "state_at_generation",
        "generated_at",
    )
    list_filter = ("explanation_type", "state_at_generation")
    readonly_fields = ("generated_at",)
