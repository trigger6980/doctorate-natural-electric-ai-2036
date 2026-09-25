# Off-Grid AI Box (Portable Self-Powered Intelligence Node)

**Natural Electric prototype #2** — A portable, multi-source-powered AI-in-a-box capable of running local models with zero external connectivity after initial provisioning.

## Design Goals
- Power sources: solar panel, hand-crank, battery bank, USB input (any combination).
- Compute: sufficient for at least one useful local LLM or specialized TinyML/agent stack at interactive speeds on constrained hardware.
- Interfaces: optional camera, mic, speaker, display or headless + BLE/USB.
- Rugged, portable, minimal external cables.
- Fully offline after models and knowledge are loaded.

## Reference Inspiration (2025–2026 open designs)
- Solar + hand-crank + battery power banks paired with compact Android/Linux compute (e.g. XREAL Beam-class or Raspberry Pi / Orange Pi class devices).
- Quantized local LLMs via llama.cpp / Ollama / MLC-LLM style runtimes.
- Energy-aware duty cycling from the companion energy-harvester-tinyml work.

## Minimum Viable Hardware Path
1. Compute: Raspberry Pi Zero 2W or equivalent low-power SBC / Android compute module.
2. Power: commercial solar + hand-crank power bank (or discrete solar + MPPT + LiPo + hand-crank generator).
3. Storage: sufficient for one or more quantized models (8–32 GB class).
4. I/O: optional small display or pure headless with Bluetooth/USB keyboard.

See [`BOM.md`](BOM.md) for a commodity parts orientation (not a store SKU).

## Software Stack (planned)
- Local model runtime (llama.cpp or equivalent).
- Energy-state monitoring service (shared with energy-harvester-tinyml concepts).
- Simple agent or RAG layer that works entirely offline.
- Secure erase and integrity tools from the SECURITY track.

Host stub now in-tree: [`energy_duty.py`](energy_duty.py) decides SLEEP / IDLE_LISTEN / INFER / REFUSE from a caller-supplied pack voltage. It does **not** read an ADC. Tests: [`test_energy_duty.py`](test_energy_duty.py).

## Status
Outline plus BOM orientation plus a host energy-duty stub. Enclosure notes, first-boot scripts, and measured idle current are still open. No field endurance numbers.
