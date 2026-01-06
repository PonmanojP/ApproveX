from django.contrib import admin
from .models import ApprovalRequest, ApprovalAction


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "bonafide_type",
        "current_state",
        "created_at",
        "final_decision_at",
    )
    list_filter = ("bonafide_type", "current_state")
    search_fields = ("student__username", "student__roll_number")
    readonly_fields = ("created_at", "updated_at", "final_decision_at")


@admin.register(ApprovalAction)
class ApprovalActionAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "actor",
        "action",
        "state_at_action",
        "created_at",
    )
    list_filter = ("action", "state_at_action")
    search_fields = ("actor__username",)
    readonly_fields = ("created_at",)
