from django.contrib import admin
from .models import UploadedDocument


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "document_type",
        "uploaded_by",
        "version",
        "uploaded_at",
    )
    list_filter = ("document_type",)
    search_fields = ("document_type", "uploaded_by__username")
    readonly_fields = ("uploaded_at",)
