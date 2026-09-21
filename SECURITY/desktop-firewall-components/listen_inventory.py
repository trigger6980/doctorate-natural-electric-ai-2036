"""Read-only inventory of TCP listeners from Linux /proc/net/tcp{,6}.

This module does not open sockets, change firewall rules, or scan remote hosts.
It exists so an off-grid operator can see what is already bound locally.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

PROC_TCP = Path("/proc/net/tcp")
PROC_TCP6 = Path("/proc/net/tcp6")
LISTEN_STATE = "0A"


def _parse_hex_ipv4(addr_hex: str) -> str:
    raw = bytes.fromhex(addr_hex)
    return ".".join(str(b) for b in raw[::-1])


def _parse_hex_port(port_hex: str) -> int:
    return int(port_hex, 16)


def parse_proc_net_tcp(text: str, *, ipv6: bool = False) -> List[Tuple[str, int]]:
    """Parse a /proc/net/tcp or tcp6 snapshot. Returns (addr, port) for LISTEN only."""
    listeners: List[Tuple[str, int]] = []
    lines = text.splitlines()
    if not lines:
        return listeners
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[1]
        state = parts[3]
        if state != LISTEN_STATE:
            continue
        if ":" not in local:
            continue
        addr_hex, port_hex = local.split(":", 1)
        try:
            port = _parse_hex_port(port_hex)
        except ValueError:
            continue
        if ipv6:
            addr = addr_hex.lower()
        else:
            try:
                addr = _parse_hex_ipv4(addr_hex)
            except ValueError:
                continue
        listeners.append((addr, port))
    return listeners


def read_live_listeners(paths: Iterable[Path] | None = None) -> List[Tuple[str, int]]:
    """Read live /proc files if present. Missing files yield no rows."""
    if paths is None:
        paths = (PROC_TCP, PROC_TCP6)
    found: List[Tuple[str, int]] = []
    for path in paths:
        if not path.is_file():
            continue
        ipv6 = path.name.endswith("6")
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found.extend(parse_proc_net_tcp(text, ipv6=ipv6))
    return found


def format_listeners(rows: List[Tuple[str, int]]) -> str:
    if not rows:
        return "No TCP listeners found (or /proc not available on this host).\n"
    lines = ["addr\tport"]
    for addr, port in rows:
        lines.append(f"{addr}\t{port}")
    return "\n".join(lines) + "\n"


def main() -> int:
    print(format_listeners(read_live_listeners()), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
