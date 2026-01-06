# workflow/state_machine.py

from approval_requests.models import RequestState, ApprovalAction
from audit.models import AuditEvent
from django.utils import timezone


ALLOWED_TRANSITIONS = {
    RequestState.DRAFT: [
        RequestState.SUBMITTED,
    ],

    RequestState.SUBMITTED: [
        RequestState.AI_VALIDATION_FAILED,
        RequestState.AWAITING_TUTOR_REVIEW,
    ],

    RequestState.AI_VALIDATION_FAILED: [
        RequestState.SUBMITTED,
    ],

    RequestState.AWAITING_TUTOR_REVIEW: [
        RequestState.AWAITING_PC_APPROVAL,
        RequestState.AWAITING_STUDENT_UPDATE,
        RequestState.REJECTED,
    ],

    RequestState.AWAITING_STUDENT_UPDATE: [
        RequestState.SUBMITTED,
    ],

    RequestState.AWAITING_PC_APPROVAL: [
        RequestState.AWAITING_HOD_APPROVAL,
        RequestState.AWAITING_TUTOR_REVIEW,
        RequestState.REJECTED,
    ],

    RequestState.AWAITING_HOD_APPROVAL: [
        RequestState.AWAITING_DEAN_APPROVAL,
        RequestState.AWAITING_TUTOR_REVIEW,
        RequestState.APPROVED,
        RequestState.REJECTED,
    ],

    RequestState.AWAITING_DEAN_APPROVAL: [
        RequestState.AWAITING_TUTOR_REVIEW,
        RequestState.APPROVED,
        RequestState.REJECTED,
    ],
}

ROLE_STATE_ACCESS = {
    RequestState.AWAITING_TUTOR_REVIEW: ["TUTOR"],
    RequestState.AWAITING_PC_APPROVAL: ["PC"],
    RequestState.AWAITING_HOD_APPROVAL: ["HOD"],
    RequestState.AWAITING_DEAN_APPROVAL: ["DEAN"],
}

def transition_request(
    request,
    to_state,
    actor,
    action=None,
    comment=None,
):
    from_state = request.current_state

    # 1️⃣ Validate transition
    allowed = ALLOWED_TRANSITIONS.get(from_state, [])
    if to_state not in allowed:
        raise ValueError(
            f"Invalid transition from {from_state} to {to_state}"
        )

    # 2️⃣ Validate role authority (if applicable)
    required_roles = ROLE_STATE_ACCESS.get(from_state)
    if required_roles and actor.role not in required_roles:
        raise PermissionError(
            f"{actor.role} cannot act on state {from_state}"
        )

    # 3️⃣ Update request state
    request.current_state = to_state

    if to_state in [RequestState.APPROVED, RequestState.REJECTED]:
        request.final_decision_at = timezone.now()

    request.save()

    # 4️⃣ Log approval action (if human-triggered)
    if action:
        ApprovalAction.objects.create(
            request=request,
            actor=actor,
            action=action,
            comment=comment,
            state_at_action=from_state,
        )

    # 5️⃣ Audit event
    AuditEvent.objects.create(
        request=request,
        actor=actor,
        action=f"STATE_CHANGE: {from_state} → {to_state}",
        metadata={
            "action": action,
            "comment": comment,
        },
    )

    return request
