"""Model 50 host checklist: six inquiry-completeness items.

This is not a CRM, not a quote, and not a contract.
"""

from __future__ import annotations

from typing import Mapping

REQUIRED = (
    "model_ids",
    "license_shape",
    "deploy_context",
    "energy_honesty",
    "scope_table",
    "deliverable_shape",
)

ALLOWED_SHAPES = {"identical", "custom", "undecided"}
ALLOWED_DELIVERABLES = {
    "research_replica",
    "field_custom",
    "operator_integration",
    "sovereign",
}
ALLOWED_HONESTY = {"agreed", "to-be-measured", "out of scope"}
OBSERVER_EVIDENCE_TOKENS = {
    "observer",
    "energy_observer",
    "energy_observer.json",
    "host_placeholder",
    "hardware_pending",
    "sandbox_observer",
    "claim_scan",
}
# Same refused set as AGENTS/claim_gate.REFUSED_CLAIMS.
REFUSED_INTENDED_USE = {
    "field_generation",
    "quote_evidence",
    "result_record",
}
ALLOWED_INTENDED_USE = {
    "host_log",
    "sandbox_demo",
    "discuss",
    "ask",
}


def _filled(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    return True


def _evidence_token(inquiry: Mapping[str, object]) -> str:
    raw = inquiry.get("energy_evidence", "")
    if isinstance(raw, str):
        return raw.strip().lower()
    return ""


def _intended_use(inquiry: Mapping[str, object]) -> str:
    raw = inquiry.get("intended_use", "")
    if isinstance(raw, str):
        return raw.strip().lower()
    return ""


def items_present(inquiry: Mapping[str, object]) -> int:
    return sum(1 for key in REQUIRED if _filled(inquiry.get(key)))


def refuse_reason(inquiry: Mapping[str, object]) -> str:
    if inquiry.get("wellbeing_ok") is False:
        return "wellbeing"
    if _evidence_token(inquiry) in OBSERVER_EVIDENCE_TOKENS:
        return "observer_not_evidence"
    use = _intended_use(inquiry)
    if use in REFUSED_INTENDED_USE:
        return "observer_not_evidence"
    if use and use not in ALLOWED_INTENDED_USE:
        return "unknown_claim"
    missing_map = {
        "model_ids": "missing_model",
        "license_shape": "missing_shape",
        "deploy_context": "missing_context",
        "energy_honesty": "missing_honesty",
        "scope_table": "missing_scope",
        "deliverable_shape": "missing_deliverable",
    }
    for key, token in missing_map.items():
        if not _filled(inquiry.get(key)):
            return token
    shape = str(inquiry.get("license_shape", "")).strip()
    if shape not in ALLOWED_SHAPES:
        return "missing_shape"
    deliverable = str(inquiry.get("deliverable_shape", "")).strip()
    if deliverable not in ALLOWED_DELIVERABLES:
        return "missing_deliverable"
    honesty = inquiry.get("energy_honesty")
    if isinstance(honesty, str) and honesty not in ALLOWED_HONESTY:
        return "missing_honesty"
    return "ok"


def inquiry_ok(inquiry: Mapping[str, object]) -> bool:
    """True only when a quote *draft* may be considered."""
    return refuse_reason(inquiry) == "ok"


def quote_action(inquiry: Mapping[str, object]) -> str:
    reason = refuse_reason(inquiry)
    if reason == "wellbeing":
        return "decline"
    if reason in {"observer_not_evidence", "unknown_claim"}:
        return "ask"
    if reason == "ok":
        return "draft"
    if reason == "unknown":
        return "unknown"
    return "ask"


def stamp(inquiry: Mapping[str, object]) -> dict:
    """Host label packet. Not a quote, contract, or energy certificate."""
    use = _intended_use(inquiry)
    return {
        "items_present": items_present(inquiry),
        "items_required": len(REQUIRED),
        "refuse_reason": refuse_reason(inquiry),
        "quote_action": quote_action(inquiry),
        "intended_use": use or None,
        "energy_evidence": _evidence_token(inquiry) or None,
        "inquiry_ok": inquiry_ok(inquiry),
        "note": (
            "Host completeness stamp only. draft is permission to write questions "
            "into a quote outline, not a price, SLA, or measured joule figure."
        ),
    }
