from django.db import models
from accounts.models import User
from approval_requests.models import ApprovalRequest
from requirements_engine.models import RequirementVersion

class AuditEvent(models.Model):
    request = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name="audit_events"
    )

    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    action = models.CharField(max_length=100)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} | {self.request}"

class AIExplanation(models.Model):
    request = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name="ai_explanations"
    )

    requirement_version = models.ForeignKey(
        RequirementVersion,
        on_delete=models.SET_NULL,
        null=True
    )

    state_at_generation = models.CharField(max_length=50)
    explanation_type = models.CharField(max_length=50)
    explanation_text = models.TextField()
    structured_insight = models.JSONField(blank=True, null=True)

    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.explanation_type} | {self.request}"
