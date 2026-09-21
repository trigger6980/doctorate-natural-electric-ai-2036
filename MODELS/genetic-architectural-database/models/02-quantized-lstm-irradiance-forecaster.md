# 02 — Quantized LSTM Irradiance Forecaster

**Domain:** TinyML + Energy Harvest Prediction  
**Energy Profile:** Low  
**Status:** Catalog + interface specification (no trained weights in-tree yet)  
**Operator role:** Harvest-forecast plug-in that feeds Model 01 / later learned policies

## Description
Lightweight LSTM (or GRU) quantized to int8, trained to forecast short-horizon solar / indoor lux from recent measurements. Output feeds the energy-aware scheduler so the node can plan duty cycles ahead of irradiance changes.

This card specifies the *intended* host and MCU interface. There is **no trained checkpoint in this repository yet**. Numbers below are design targets, not measured results.

## Interface (planned)

| Symbol | Kind | Notes |
| --- | --- | --- |
| `lux_window[T]` | input | Last T lux samples (T target = 16) |
| `dt_s` | input | Sample interval in seconds |
| `voltage_v` | optional input | Used only to decide whether inference may run |
| `horizon_steps` | parameter | Default 4 (one-step to four-step ahead) |
| `forecast_lux[]` | output | Predicted lux for the next horizon |
| `confidence` | output | Optional 0–1 score; omitted until calibrated |

Python / MCU entry points (planned names):
- `forecast_lux(window, dt_s, horizon=4) -> list[float]`
- `may_run(energy_state) -> bool` — refuse inference when Model 01 would choose SLEEP

## Energy budget (example, not measured hardware)
These numbers are **placeholders**. They must be replaced with bench measurements on the target board before any production claim.

| Action | Simulator / target cost | Intended physical meaning |
| --- | --- | --- |
| Load int8 weights from flash | 0.001 J | One-time per wake if not already resident |
| Forward pass (16-step window) | 0.006–0.012 J | Target on ESP32-class MCU |
| Skip (policy = SLEEP) | 0 J extra | Gate via Model 01 |

Safety rule: never run the forecaster when `voltage_v < v_min_safe` from Model 01.

## Key Traits
- Model size target < 50 KB
- Inference cost target in low single-digit mJ on ESP32-class MCUs
- Designed for intermittent execution
- Output is a harvest *hint*, not a guarantee of incoming joules

## Implementation Notes
Not implemented. When added, live under `PROTOTYPES/energy-harvester-tinyml/` and be invoked only after the policy gate in `AGENTS/policy_gated_executor.py` allows INFER.

## Next measurements (not done)
- Collect indoor + outdoor lux traces with timestamps.
- Train a tiny GRU/LSTM offline; export int8.
- Measure forward-pass joules on the same board used for Model 01.
