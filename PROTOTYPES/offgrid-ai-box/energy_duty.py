"""Host energy-duty stub for the Off-Grid AI Box.

Not a hardware observer. Inputs are caller-supplied volts / watts.
Refuse inference when the pack proxy is below the documented floor.
"""

from __future__ import annotations

FLOOR_VOLTS = 3.50  # documented placeholder for a 1S Li-ion proxy; not a lab calibration
IDLE_WATTS_DEFAULT = 1.5
INFER_WATTS_DEFAULT = 4.0

ACTIONS = ("SLEEP", "IDLE_LISTEN", "INFER", "REFUSE")


def decide(
    pack_volts: float,
    *,
    infer_requested: bool = False,
    floor_volts: float = FLOOR_VOLTS,
) -> str:
    """Return a duty action. Low voltage always wins."""
    if pack_volts < 0:
        raise ValueError("pack_volts must be >= 0")
    if pack_volts < floor_volts:
        return "REFUSE" if infer_requested else "SLEEP"
    if infer_requested:
        return "INFER"
    return "IDLE_LISTEN"


def hours_remaining(
    pack_wh: float,
    *,
    infer_requested: bool = False,
    idle_w: float = IDLE_WATTS_DEFAULT,
    infer_w: float = INFER_WATTS_DEFAULT,
) -> float:
    """Placeholder endurance. Watts are assumptions, not measured."""
    if pack_wh < 0:
        raise ValueError("pack_wh must be >= 0")
    load = infer_w if infer_requested else idle_w
    if load <= 0:
        raise ValueError("load watts must be > 0")
    return pack_wh / load
