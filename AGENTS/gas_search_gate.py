"""Model 49 host stub: gas_ok on a fixture candidate table.

This is not a NAS controller, not AutoML, and not an architecture certificate.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

ALLOWED_ROW_STATUS = {"agreed", "to-be-measured", "out of scope"}
KNOWN_WAKE = {"hold", "keep_parent", "mutate", "defer"}


def _rows(search_table: object) -> Sequence[Mapping[str, Any]]:
    if not isinstance(search_table, Sequence) or isinstance(search_table, (str, bytes)):
        return ()
    return [row for row in search_table if isinstance(row, Mapping)]


def refuse_reason(
    energy_state: Mapping[str, Any] | None,
    search_table: object,
    hold_gas: str | None = None,
    *,
    energy_grant_ok: bool = True,
    scr_ok: bool = True,
    hmo_ok: bool = True,
    att_ok: bool = True,
    rst_ok: bool = True,
    ctr_ok: bool = True,
    airgap_required: bool = False,
    wake_class: str | None = None,
    v_min_safe: float = 3.3,
) -> str:
    """Return a refuse token. 'ok' means the named table may be walked."""
    if energy_state is None:
        return "energy"
    try:
        voltage = float(energy_state.get("rail_voltage_v", energy_state.get("voltage_v", 0.0)))
    except (TypeError, ValueError):
        return "energy"
    if voltage < v_min_safe:
        return "energy"

    if energy_grant_ok is False:
        return "grant"
    if scr_ok is False:
        return "slot"
    if hmo_ok is False:
        return "hierarchy"
    if att_ok is False:
        return "attest"
    if rst_ok is False:
        return "restart"
    if ctr_ok is False:
        return "contract"

    if wake_class is not None and wake_class not in KNOWN_WAKE:
        return "unknown"

    rows = _rows(search_table)
    if not rows:
        return "missing_table"

    hold = (hold_gas or "").strip()
    for row in rows:
        status = str(row.get("status", "")).strip()
        if status not in ALLOWED_ROW_STATUS:
            return "missing_table"
        needs_pull = bool(row.get("needs_outbound_dataset"))
        if airgap_required and needs_pull:
            return "airgap"
        if status == "to-be-measured":
            if not hold:
                return "no_hold"
            named = str(row.get("hold_id", "")).strip()
            if named and named != hold:
                return "unmeasured"
    return "ok"


def gas_ok(
    energy_state: Mapping[str, Any] | None,
    search_table: object,
    hold_gas: str | None = None,
    **kwargs: Any,
) -> bool:
    """True only when the next scheduled generation may run under the named table."""
    return refuse_reason(energy_state, search_table, hold_gas, **kwargs) == "ok"


def gas_action(
    energy_state: Mapping[str, Any] | None,
    search_table: object,
    hold_gas: str | None = None,
    **kwargs: Any,
) -> str:
    reason = refuse_reason(energy_state, search_table, hold_gas, **kwargs)
    if reason != "ok":
        if reason == "unknown":
            return "unknown"
        if reason == "energy":
            return "defer"
        return "hold"
    wake = kwargs.get("wake_class") or "hold"
    if wake not in KNOWN_WAKE:
        return "unknown"
    return wake
