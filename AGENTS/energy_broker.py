"""
Model 11 host stub: partition one energy pool among local agents.

No radio, no consensus, no hardware. Grants never exceed
max(0, pool_j - reserve_j). Priority is an integer; larger wins.
Equal priority keeps request order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class EnergyRequest:
    agent_id: str
    want_j: float
    priority: int = 0


@dataclass(frozen=True)
class EnergyGrant:
    agent_id: str
    granted_j: float


def estimate_broker_cost_j(n_requests: int) -> float:
    """Placeholder table lookup. Not a measured MCU cost."""
    if n_requests < 0:
        raise ValueError("n_requests must be non-negative")
    return 0.0002 * float(n_requests)


def allocate(
    pool_j: float,
    requests: Iterable[EnergyRequest],
    reserve_j: float = 0.0,
) -> List[EnergyGrant]:
    """Greedy priority allocator. Deterministic. Never over-grants."""
    if pool_j < 0.0:
        raise ValueError("pool_j must be non-negative")
    if reserve_j < 0.0:
        raise ValueError("reserve_j must be non-negative")

    reqs = list(requests)
    for r in reqs:
        if r.want_j < 0.0:
            raise ValueError(f"want_j must be non-negative for {r.agent_id}")

    available = max(0.0, pool_j - reserve_j)
    # Stable: original index breaks priority ties.
    ordered = sorted(enumerate(reqs), key=lambda item: (-item[1].priority, item[0]))
    granted = {r.agent_id: 0.0 for r in reqs}

    for _, req in ordered:
        if available <= 0.0:
            break
        take = min(req.want_j, available)
        granted[req.agent_id] = take
        available -= take

    return [EnergyGrant(agent_id=r.agent_id, granted_j=granted[r.agent_id]) for r in reqs]
