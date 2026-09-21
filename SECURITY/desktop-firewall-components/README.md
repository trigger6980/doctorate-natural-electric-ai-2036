# Desktop Firewall & Networking Components

**Natural Electric / Sovereign Compute security track**

## Intent
Provide lightweight, auditable desktop and edge components that improve firewall, networking, and high-speed local connectivity while remaining suitable for air-gapped or intermittently connected environments.

## Planned Modules
- Packet filter configuration helpers and audit logging
- Local high-speed mesh / point-to-point helpers (no cloud dependency)
- One-off security utilities (key generation, secure erase patterns, integrity checkers)
- Documentation for integrating with off-grid AI boxes and home-lab microgrids

## Current module: read-only listen inventory
`listen_inventory.py` lists TCP listeners from `/proc/net/tcp` and `/proc/net/tcp6` (Linux host). It is **read-only**: it does not open sockets, change iptables, or describe exploits.

```
python3 listen_inventory.py
python3 -m unittest test_listen_inventory.py
```

On non-Linux hosts the parser still accepts fixture text (used by the unit test). Live `/proc` reads simply return an empty list if those files are absent.

## Status
First concrete utility is the listen inventory. Packet-filter helpers remain planned and are not implemented.

## Design Principles
- Prefer readable, reviewable code over heavy frameworks
- No mandatory external network calls
- Clear failure modes and offline operation
- Inventory and audit before any mutate path
