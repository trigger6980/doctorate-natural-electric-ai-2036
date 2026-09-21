# 02 — Quantized LSTM Irradiance Forecaster

**Domain:** TinyML + Energy Harvest Prediction  
**Energy Profile:** Low  
**Status:** Catalog entry (implementation planned)

## Description
Lightweight LSTM (or GRU) quantized to int8, trained to forecast short-horizon solar / indoor lux from recent measurements. Output feeds the energy-aware scheduler so the node can plan duty cycles ahead of irradiance changes.

## Key Traits
- Model size target < 50 KB
- Inference cost measured in low single-digit mJ on ESP32-class MCUs
- Designed for intermittent execution
