from django.db import models
from accounts.models import User
from requirements_engine.models import RequirementVersion


class RequestState(models.TextChoices):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    AI_VALIDATION_FAILED = "AI_VALIDATION_FAILED"
    AWAITING_TUTOR_REVIEW = "AWAITING_TUTOR_REVIEW"
    AWAITING_STUDENT_UPDATE = "AWAITING_STUDENT_UPDATE"
    AWAITING_PC_APPROVAL = "AWAITING_PC_APPROVAL"
    AWAITING_HOD_APPROVAL = "AWAITING_HOD_APPROVAL"
    AWAITING_DEAN_APPROVAL = "AWAITING_DEAN_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class BonafideType(models.TextChoices):
    DEPARTMENT = "DEPARTMENT"
    COLLEGE = "COLLEGE"


class ApprovalRequest(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="approval_requests"
    )

    bonafide_type = models.CharField(
        max_length=20, choices=BonafideType.choices
    )

    current_state = models.CharField(
        max_length=50, choices=RequestState.choices
    )

    current_requirement_version = models.ForeignKey(
        RequirementVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    final_decision_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} | {self.student} | {self.bonafide_type}"

class ApprovalAction(models.Model):
    request = models.ForeignKey(
        ApprovalRequest, on_delete=models.CASCADE, related_name="actions"
    )

    actor = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=20,
        choices=[
            ("APPROVED", "Approved"),
            ("REJECTED", "Rejected"),
            ("COMMENTED", "Commented"),
        ]
    )

    comment = models.TextField(blank=True, null=True)
    state_at_action = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.actor} at {self.state_at_action}"
