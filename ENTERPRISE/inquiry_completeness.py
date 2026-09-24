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

# Section keys from ENTERPRISE/quote-draft-outline.md. Host labels only.
OUTLINE_SECTIONS = (
    "parties_and_date",
    "model_numbers_and_ancestry",
    "identical_vs_custom",
    "deliverable_shape",
    "in_scope_files",
    "out_of_scope",
    "energy_honesty_table",
    "who_measures_joules",
    "commercial_figure_off_repo",
    "what_stays_public",
)

# Only this section is never fillable in the public tree.
OFF_REPO_SECTIONS = frozenset({"commercial_figure_off_repo"})

LANE_PUBLIC = "public_fill"
LANE_OFF_REPO = "off_repo"
LANE_NOT_READY = "not_ready"
LANE_UNKNOWN = "unknown_section"


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


def outline_ready(inquiry: Mapping[str, object]) -> dict:
    """Whether a quote *outline* may be filled. Never a price or SLA."""
    action = quote_action(inquiry)
    return {
        "outline_ready": action == "draft",
        "price_allowed": False,
        "quote_action": action,
        "sections": list(OUTLINE_SECTIONS),
        "note": (
            "outline_ready means the six completeness items passed and a maintainer "
            "may copy headings from quote-draft-outline.md. price_allowed is always "
            "false on this host helper; the commercial figure stays off-repo."
        ),
    }


def copy_headings(inquiry: Mapping[str, object]) -> dict:
    """Headings a maintainer may copy. Empty list when the outline is not ready.

    Never includes a commercial figure. Section 9 stays off-repo even when
    headings_copyable is true.
    """
    ready = outline_ready(inquiry)["outline_ready"]
    headings = list(OUTLINE_SECTIONS) if ready else []
    fill_on_repo = {
        key: (ready and key not in OFF_REPO_SECTIONS) for key in OUTLINE_SECTIONS
    }
    return {
        "headings_copyable": ready,
        "headings": headings,
        "fill_on_repo": fill_on_repo,
        "price_allowed": False,
        "note": (
            "headings_copyable only authorizes copying section titles. "
            "fill_on_repo[commercial_figure_off_repo] is always false."
        ),
    }


def public_fill_keys(inquiry: Mapping[str, object]) -> list[str]:
    """Section keys a maintainer may fill in the public tree.

    Empty when the outline is not ready. Never includes commercial_figure_off_repo.
    """
    copied = copy_headings(inquiry)
    return [key for key, allowed in copied["fill_on_repo"].items() if allowed]


def off_repo_keys(inquiry: Mapping[str, object]) -> list[str]:
    """Section keys that must stay off the public tree.

    When the outline is ready this is the OFF_REPO_SECTIONS list
    (currently only commercial_figure_off_repo). When the outline is
    not ready this is empty — there is no draft to partition.
    """
    if not outline_ready(inquiry)["outline_ready"]:
        return []
    return [key for key in OUTLINE_SECTIONS if key in OFF_REPO_SECTIONS]


def partition_keys(inquiry: Mapping[str, object]) -> dict:
    """Public vs off-repo section partition. Not a rate card.

    When the outline is ready the two lists are disjoint and their union
    equals OUTLINE_SECTIONS. When the outline is not ready both lists are
    empty and covers_outline is false. price_allowed is always false.
    """
    public = public_fill_keys(inquiry)
    off = off_repo_keys(inquiry)
    ready = outline_ready(inquiry)["outline_ready"]
    public_set = set(public)
    off_set = set(off)
    return {
        "outline_ready": ready,
        "public_fill_keys": public,
        "off_repo_keys": off,
        "disjoint": public_set.isdisjoint(off_set),
        "covers_outline": ready and (public_set | off_set) == set(OUTLINE_SECTIONS),
        "price_allowed": False,
        "note": (
            "partition_keys is a host split of outline headings. "
            "disjoint must stay true. covers_outline is true only when a draft "
            "may exist and every section is either public-fill or off-repo. "
            "price_allowed is always false; dollars stay off this tree."
        ),
    }


def section_lane(inquiry: Mapping[str, object], key: str) -> dict:
    """Which filing lane one outline heading belongs to. Not a price.

    Lanes:
    - public_fill: outline ready and the key may be written in this tree
    - off_repo: outline ready and the key is commercial_figure_off_repo
    - not_ready: outline is not ready (including refused intended_use)
    - unknown_section: key is not one of the ten outline headings
    price_allowed is always false.
    """
    token = str(key or "").strip()
    if token not in OUTLINE_SECTIONS:
        return {
            "key": token,
            "lane": LANE_UNKNOWN,
            "outline_ready": outline_ready(inquiry)["outline_ready"],
            "price_allowed": False,
        }
    if not outline_ready(inquiry)["outline_ready"]:
        return {
            "key": token,
            "lane": LANE_NOT_READY,
            "outline_ready": False,
            "price_allowed": False,
        }
    if token in OFF_REPO_SECTIONS:
        lane = LANE_OFF_REPO
    else:
        lane = LANE_PUBLIC
    return {
        "key": token,
        "lane": lane,
        "outline_ready": True,
        "price_allowed": False,
    }


def section_lanes(inquiry: Mapping[str, object]) -> dict[str, str]:
    """Map every known outline heading to its lane. Not a rate card."""
    return {key: section_lane(inquiry, key)["lane"] for key in OUTLINE_SECTIONS}


def stamp(inquiry: Mapping[str, object]) -> dict:
    """Host label packet. Not a quote, contract, or energy certificate."""
    use = _intended_use(inquiry)
    outline = outline_ready(inquiry)
    copied = copy_headings(inquiry)
    part = partition_keys(inquiry)
    return {
        "items_present": items_present(inquiry),
        "items_required": len(REQUIRED),
        "refuse_reason": refuse_reason(inquiry),
        "quote_action": quote_action(inquiry),
        "intended_use": use or None,
        "energy_evidence": _evidence_token(inquiry) or None,
        "inquiry_ok": inquiry_ok(inquiry),
        "outline_ready": outline["outline_ready"],
        "price_allowed": outline["price_allowed"],
        "outline_sections": outline["sections"],
        "headings_copyable": copied["headings_copyable"],
        "headings": copied["headings"],
        "fill_on_repo": copied["fill_on_repo"],
        "public_fill_keys": public_fill_keys(inquiry),
        "off_repo_keys": off_repo_keys(inquiry),
        "partition_disjoint": part["disjoint"],
        "partition_covers_outline": part["covers_outline"],
        "section_lanes": section_lanes(inquiry),
        "note": (
            "Host completeness stamp only. draft is permission to write questions "
            "into a quote outline, not a price, SLA, or measured joule figure. "
            "price_allowed is always false on this helper. "
            "headings_copyable only authorizes copying titles from quote-draft-outline.md. "
            "public_fill_keys never includes commercial_figure_off_repo. "
            "off_repo_keys is that commercial key when the outline is ready, else empty. "
            "partition_disjoint must stay true; partition_covers_outline is true only "
            "when a draft outline exists and every section is assigned. "
            "section_lanes maps each known heading to public_fill, off_repo, or not_ready."
        ),
    }
