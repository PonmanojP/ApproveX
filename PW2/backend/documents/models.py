from django.db import models
from accounts.models import User
from approval_requests.models import ApprovalRequest


class UploadedDocument(models.Model):
    request = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name="documents"
    )

    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    version = models.PositiveIntegerField(default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} (v{self.version})"
