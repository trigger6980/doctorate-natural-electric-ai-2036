"""Model 50 host checklist: six inquiry-completeness items.

This is not a CRM, not a quote, and not a contract.
"""

from __future__ import annotations

from typing import Any

REQUIRED = (
    "model_ids",
    "license_shape",
    "deploy_context",
    "energy_honesty",
    "scope_table",
    "deliverable_shape",
)

ALLOWED_SHAPES = frozenset({"identical", "custom", "undecided"})
ALLOWED_DELIVERABLES = frozenset(
    {"research_replica", "field_customization", "operator_integration", "sovereign"}
)
ALLOWED_USES = frozenset({"discuss", "ask", "host_log", "sandbox_demo"})
REFUSED_USES = frozenset({"field_generation", "quote_evidence", "result_record"})
OBSERVER_TOKENS = frozenset(
    {
        "observer",
        "energy_observer",
        "energy_observer.json",
        "host_placeholder",
        "hardware_pending",
        "sandbox_observer",
        "claim_scan",
    }
)

OUTLINE_SECTIONS = (
    "parties_and_date",
    "model_and_license",
    "deploy_context",
    "energy_honesty_table",
    "scope_assumptions",
    "deliverable_shape",
    "who_measures_joules",
    "what_stays_public",
    "in_scope_files",
    "commercial_figure_off_repo",
)

LANE_PUBLIC = "public_fill"
LANE_OFF_REPO = "off_repo"
LANE_NOT_READY = "not_ready"
LANE_UNKNOWN = "unknown_section"

ACTION_DECLINE = "decline"
ACTION_ASK = "ask"
ACTION_COPY_HEADINGS = "copy_headings"
ALLOWED_ACTIONS = frozenset({ACTION_DECLINE, ACTION_ASK, ACTION_COPY_HEADINGS})
BLOCKED_PRICE_VERBS = frozenset({"publish_price", "quote_price", "set_rate"})
COMMERCIAL_KEY = "commercial_figure_off_repo"


def _present(inquiry: dict[str, Any], key: str) -> bool:
    value = inquiry.get(key)
    if value is None:
        return False
    if key == "model_ids":
        return isinstance(value, list) and len(value) > 0
    if key == "license_shape":
        return value in ALLOWED_SHAPES
    if key == "deliverable_shape":
        return value in ALLOWED_DELIVERABLES
    if key == "scope_table":
        return isinstance(value, dict) and len(value) > 0
    if isinstance(value, str):
        return bool(value.strip())
    return bool(value)


def items_present(inquiry: dict[str, Any]) -> int:
    return sum(1 for key in REQUIRED if _present(inquiry, key))


def refuse_reason(inquiry: dict[str, Any]) -> str:
    if inquiry.get("wellbeing_ok") is False:
        return "wellbeing"
    evidence = inquiry.get("energy_evidence")
    if evidence in OBSERVER_TOKENS:
        return "observer_not_evidence"
    use = inquiry.get("intended_use")
    if use in REFUSED_USES:
        return "observer_not_evidence"
    if use is not None and use not in ALLOWED_USES:
        return "unknown_claim"
    if items_present(inquiry) < 6:
        if not _present(inquiry, "model_ids"):
            return "missing_model"
        if not _present(inquiry, "license_shape"):
            return "missing_shape"
        return "incomplete"
    return "ok"


def inquiry_ok(inquiry: dict[str, Any]) -> bool:
    return refuse_reason(inquiry) == "ok"


def quote_action(inquiry: dict[str, Any]) -> str:
    reason = refuse_reason(inquiry)
    if reason == "wellbeing":
        return "decline"
    if reason == "ok":
        return "draft"
    return "ask"


def outline_ready(inquiry: dict[str, Any]) -> dict[str, Any]:
    ready = quote_action(inquiry) == "draft"
    return {
        "outline_ready": ready,
        "price_allowed": False,
        "quote_action": quote_action(inquiry),
        "sections": list(OUTLINE_SECTIONS) if ready else [],
    }


def copy_headings(inquiry: dict[str, Any]) -> dict[str, Any]:
    ready = quote_action(inquiry) == "draft"
    headings = list(OUTLINE_SECTIONS) if ready else []
    fill = {key: False for key in OUTLINE_SECTIONS}
    if ready:
        for key in OUTLINE_SECTIONS:
            fill[key] = key != COMMERCIAL_KEY
    return {
        "headings_copyable": ready,
        "headings": headings,
        "fill_on_repo": fill,
        "price_allowed": False,
    }


def public_fill_keys(inquiry: dict[str, Any]) -> list[str]:
    copied = copy_headings(inquiry)
    return [key for key, allowed in copied["fill_on_repo"].items() if allowed]


def off_repo_keys(inquiry: dict[str, Any]) -> list[str]:
    if quote_action(inquiry) != "draft":
        return []
    return [COMMERCIAL_KEY]


def partition_keys(inquiry: dict[str, Any]) -> dict[str, Any]:
    public = public_fill_keys(inquiry)
    off = off_repo_keys(inquiry)
    ready = quote_action(inquiry) == "draft"
    union = set(public) | set(off)
    overlap = set(public) & set(off)
    return {
        "outline_ready": ready,
        "price_allowed": False,
        "public_fill_keys": public,
        "off_repo_keys": off,
        "disjoint": len(overlap) == 0,
        "covers_outline": union == set(OUTLINE_SECTIONS) if ready else False,
    }


def section_lane(inquiry: dict[str, Any], key: str) -> dict[str, Any]:
    ready = quote_action(inquiry) == "draft"
    if key not in OUTLINE_SECTIONS:
        lane = LANE_UNKNOWN
    elif not ready:
        lane = LANE_NOT_READY
    elif key == COMMERCIAL_KEY:
        lane = LANE_OFF_REPO
    else:
        lane = LANE_PUBLIC
    return {
        "key": key,
        "lane": lane,
        "price_allowed": False,
        "outline_ready": ready,
    }


def section_lanes(inquiry: dict[str, Any]) -> dict[str, str]:
    return {key: section_lane(inquiry, key)["lane"] for key in OUTLINE_SECTIONS}


def lane_counts(inquiry: dict[str, Any]) -> dict[str, Any]:
    lanes = section_lanes(inquiry)
    public = sum(1 for lane in lanes.values() if lane == LANE_PUBLIC)
    off = sum(1 for lane in lanes.values() if lane == LANE_OFF_REPO)
    idle = sum(1 for lane in lanes.values() if lane == LANE_NOT_READY)
    total = len(OUTLINE_SECTIONS)
    return {
        LANE_PUBLIC: public,
        LANE_OFF_REPO: off,
        LANE_NOT_READY: idle,
        "total_known": total,
        "sums_to_known": public + off + idle == total,
        "price_allowed": False,
    }


def next_maintainer_action(inquiry: dict[str, Any]) -> dict[str, Any]:
    action_name = quote_action(inquiry)
    if action_name == "decline":
        verb = ACTION_DECLINE
    elif action_name == "draft":
        verb = ACTION_COPY_HEADINGS
    else:
        verb = ACTION_ASK
    return {
        "action": verb,
        "copy_headings": verb == ACTION_COPY_HEADINGS,
        "price_allowed": False,
        "quote_action": action_name,
        "refuse_reason": refuse_reason(inquiry),
    }


def action_flags(inquiry: dict[str, Any]) -> dict[str, Any]:
    verb = next_maintainer_action(inquiry)["action"]
    flags = {
        "decline": verb == ACTION_DECLINE,
        "ask": verb == ACTION_ASK,
        "copy_headings": verb == ACTION_COPY_HEADINGS,
        "publish_price": False,
    }
    true_count = sum(1 for key in ("decline", "ask", "copy_headings") if flags[key])
    flags["exactly_one"] = true_count == 1 and flags["publish_price"] is False
    flags["price_allowed"] = False
    return flags


def action_consistent(inquiry: dict[str, Any]) -> dict[str, Any]:
    nxt = next_maintainer_action(inquiry)
    flags = action_flags(inquiry)
    true_flags = [
        name
        for name in (ACTION_DECLINE, ACTION_ASK, ACTION_COPY_HEADINGS)
        if flags[name]
    ]
    flag_verb = true_flags[0] if len(true_flags) == 1 else None
    match = (
        nxt["action"] == flag_verb
        and flags["exactly_one"] is True
        and flags["publish_price"] is False
    )
    return {
        "match": match,
        "verb": nxt["action"],
        "flag_verb": flag_verb,
        "exactly_one": flags["exactly_one"],
        "publish_price": False,
        "price_allowed": False,
    }


def price_verbs_blocked(inquiry: dict[str, Any]) -> dict[str, Any]:
    """True when the filing verb is decline/ask/copy_headings and never a price verb."""
    nxt = next_maintainer_action(inquiry)
    flags = action_flags(inquiry)
    verb = nxt["action"]
    blocked = (
        verb in ALLOWED_ACTIONS
        and verb not in BLOCKED_PRICE_VERBS
        and flags["publish_price"] is False
        and nxt["price_allowed"] is False
    )
    return {
        "ok": blocked,
        "verb": verb,
        "allowed_verbs": sorted(ALLOWED_ACTIONS),
        "blocked_verbs": sorted(BLOCKED_PRICE_VERBS),
        "publish_price": False,
        "price_allowed": False,
    }


def commercial_figure_blank(inquiry: dict[str, Any]) -> dict[str, Any]:
    """On-repo value of the commercial-figure heading is always None. Not a price."""
    copied = copy_headings(inquiry)
    off = off_repo_keys(inquiry)
    blank = (
        copied["fill_on_repo"][COMMERCIAL_KEY] is False
        and COMMERCIAL_KEY not in public_fill_keys(inquiry)
    )
    return {
        "ok": blank,
        "key": COMMERCIAL_KEY,
        "on_repo_value": None,
        "fill_on_repo": False,
        "off_repo_when_ready": COMMERCIAL_KEY in off,
        "outline_ready": quote_action(inquiry) == "draft",
        "publish_price": False,
        "price_allowed": False,
    }


def commercial_lane_sealed(inquiry: dict[str, Any]) -> dict[str, Any]:
    """Commercial heading never uses the public_fill lane. Not a price."""
    figure = commercial_figure_blank(inquiry)
    lane = section_lane(inquiry, COMMERCIAL_KEY)["lane"]
    ready = quote_action(inquiry) == "draft"
    expected = LANE_OFF_REPO if ready else LANE_NOT_READY
    sealed = (
        figure["ok"] is True
        and figure["on_repo_value"] is None
        and COMMERCIAL_KEY not in public_fill_keys(inquiry)
        and lane == expected
        and lane != LANE_PUBLIC
    )
    return {
        "ok": sealed,
        "key": COMMERCIAL_KEY,
        "lane": lane,
        "expected_lane": expected,
        "never_public_fill": lane != LANE_PUBLIC,
        "on_repo_value": None,
        "publish_price": False,
        "price_allowed": False,
    }


def lane_fill_aligned(inquiry: dict[str, Any]) -> dict[str, Any]:
    """fill_on_repo[key] is True iff the lane is public_fill. Not a price."""
    copied = copy_headings(inquiry)
    lanes = section_lanes(inquiry)
    mismatches = []
    for key in OUTLINE_SECTIONS:
        fill = copied["fill_on_repo"][key]
        should_fill = lanes[key] == LANE_PUBLIC
        if fill is not should_fill:
            mismatches.append(key)
    aligned = (
        len(mismatches) == 0
        and copied["fill_on_repo"][COMMERCIAL_KEY] is False
        and lanes[COMMERCIAL_KEY] != LANE_PUBLIC
    )
    return {
        "ok": aligned,
        "mismatches": mismatches,
        "commercial_fill": False,
        "commercial_lane": lanes[COMMERCIAL_KEY],
        "publish_price": False,
        "price_allowed": False,
    }


def stamp_invariants(inquiry: dict[str, Any]) -> dict[str, Any]:
    """Host coherence check for stamp fields. Not a published dollar amount."""
    consistent = action_consistent(inquiry)
    flags = action_flags(inquiry)
    part = partition_keys(inquiry)
    counts = lane_counts(inquiry)
    verbs = price_verbs_blocked(inquiry)
    figure = commercial_figure_blank(inquiry)
    sealed = commercial_lane_sealed(inquiry)
    aligned = lane_fill_aligned(inquiry)
    covers_or_idle = part["covers_outline"] or (
        not part["outline_ready"] and counts[LANE_NOT_READY] == len(OUTLINE_SECTIONS)
    )
    ok = (
        consistent["match"] is True
        and flags["exactly_one"] is True
        and part["disjoint"] is True
        and covers_or_idle
        and counts["sums_to_known"] is True
        and flags["publish_price"] is False
        and verbs["ok"] is True
        and figure["ok"] is True
        and figure["on_repo_value"] is None
        and sealed["ok"] is True
        and sealed["lane"] != LANE_PUBLIC
        and aligned["ok"] is True
        and aligned["mismatches"] == []
    )
    return {
        "ok": ok,
        "action_consistent": consistent["match"],
        "exactly_one": flags["exactly_one"],
        "partition_disjoint": part["disjoint"],
        "covers_outline": part["covers_outline"],
        "covers_or_idle": covers_or_idle,
        "sums_to_known": counts["sums_to_known"],
        "price_verbs_blocked": verbs["ok"],
        "commercial_figure_blank": figure["ok"],
        "commercial_lane_sealed": sealed["ok"],
        "lane_fill_aligned": aligned["ok"],
        "publish_price": False,
        "price_allowed": False,
    }


def stamp(inquiry: dict[str, Any]) -> dict[str, Any]:
    copied = copy_headings(inquiry)
    part = partition_keys(inquiry)
    nxt = next_maintainer_action(inquiry)
    flags = action_flags(inquiry)
    consistent = action_consistent(inquiry)
    invariants = stamp_invariants(inquiry)
    verbs = price_verbs_blocked(inquiry)
    figure = commercial_figure_blank(inquiry)
    sealed = commercial_lane_sealed(inquiry)
    aligned = lane_fill_aligned(inquiry)
    return {
        "items_present": items_present(inquiry),
        "refuse_reason": refuse_reason(inquiry),
        "quote_action": quote_action(inquiry),
        "intended_use": inquiry.get("intended_use"),
        "energy_evidence": inquiry.get("energy_evidence"),
        "inquiry_ok": inquiry_ok(inquiry),
        "outline_ready": quote_action(inquiry) == "draft",
        "price_allowed": False,
        "outline_sections": list(OUTLINE_SECTIONS),
        "headings_copyable": copied["headings_copyable"],
        "headings": copied["headings"],
        "fill_on_repo": copied["fill_on_repo"],
        "public_fill_keys": public_fill_keys(inquiry),
        "off_repo_keys": off_repo_keys(inquiry),
        "partition_disjoint": part["disjoint"],
        "partition_covers_outline": part["covers_outline"],
        "covers_or_idle": invariants["covers_or_idle"],
        "section_lanes": section_lanes(inquiry),
        "lane_counts": lane_counts(inquiry),
        "next_action": nxt["action"],
        "next_action_copy_headings": nxt["copy_headings"],
        "action_flags": flags,
        "action_exactly_one": flags["exactly_one"],
        "action_consistent": consistent["match"],
        "action_flag_verb": consistent["flag_verb"],
        "price_verbs_blocked": verbs["ok"],
        "price_verbs": verbs,
        "commercial_figure_blank": figure["ok"],
        "commercial_figure": figure,
        "commercial_lane_sealed": sealed["ok"],
        "commercial_lane": sealed,
        "lane_fill_aligned": aligned["ok"],
        "lane_fill": aligned,
        "stamp_invariants_ok": invariants["ok"],
        "stamp_invariants": invariants,
    }
