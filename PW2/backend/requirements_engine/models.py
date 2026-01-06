from django.db import models
from accounts.models import User


class RequirementSet(models.Model):
    REQUEST_TYPE_CHOICES = [
        ("BONAFIDE", "Bonafide"),
    ]

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    bonafide_type = models.CharField(
        max_length=20,
        choices=[
            ("DEPARTMENT", "Department"),
            ("COLLEGE", "College"),
        ]
    )

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_type} | {self.bonafide_type}"

class RequirementVersion(models.Model):
    requirement_set = models.ForeignKey(
        RequirementSet,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    version = models.PositiveIntegerField()
    rules = models.JSONField()
    change_reason = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("requirement_set", "version")

    def __str__(self):
        return f"{self.requirement_set} v{self.version}"
