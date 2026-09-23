# Generator 01 — Solar Thermal Thermosiphon + Batch — Detailed Design

**Dyad process:** Lumen expanded collector sizing, passive circulation rules, and climate adaptations. Aegis enforced freeze-protection realism, stagnation safety, and reproducible BOM constraints.

## 1. Collector Sizing (Rule-of-Thumb + Climate Adjustment)

| Daily Hot Water Demand | Mild Climate (e.g. 4–5 kWh/m²/day) | Moderate | Cold / Cloudy |
|------------------------|-------------------------------------|----------|---------------|
| 50 L at 45–50 °C      | 1.0–1.5 m²                         | 1.5–2.0 m² | 2.5–3.5 m²   |
| 100 L                  | 2.0–2.5 m²                         | 3.0–4.0 m² | 5.0–6.5 m²   |
| 150 L                  | 3.0–3.5 m²                         | 4.5–5.5 m² | 7.0–9.0 m²   |

- Use selective-surface flat-plate or evacuated-tube collectors.
- Tilt = latitude (or latitude + 10–15° for winter bias).
- Face true south (northern hemisphere) or true north (southern).

## 2. Thermosiphon Rules (Critical for Passive Operation)
- Collector below tank (vertical distance 30–60 cm minimum recommended).
- Riser pipe continuously rises; no dips.
- Pipe diameter typically 18–28 mm for domestic systems; larger for higher flow.
- Insulation on all pipes mandatory.
- Maximum practical height difference ~3–4 m before friction losses become problematic.

## 3. Freeze-Protection Strategies (Aegis-prioritized)

**Preferred (passive / low-maintenance):**
1. Drain-back system — water drains into tank or reservoir when circulation stops (requires careful pipe slope).
2. Closed-loop glycol (propylene glycol, food-grade) with heat exchanger in tank — most reliable in hard-freeze climates.
3. Freeze-tolerant collectors + careful pipe layout (only for mild freeze risk).

**Avoid:** Simple water-filled systems in climates that reach ≤0 °C without active protection.

**Additional protections:**
- Collector sensor + controller that forces circulation or drains if temperature approaches freezing.
- Pipe insulation rated for local minimum temperatures.
- Vacuum-breaker and proper venting on drain-back designs.

## 4. Stagnation & Overheat Protection
- High-temperature rated components (or pressure-relief + heat dump).
- Optional differential controller that stops circulation or diverts to a heat dump (radiator, swimming pool, thermal mass) when tank reaches set-point.
- Evacuated tubes can reach very high stagnation temperatures — design accordingly.

## 5. Sensors for Energy-Aware Integration
- Collector outlet temperature
- Tank top and bottom temperatures
- Optional ambient and irradiance
These feed the threshold / RL energy-aware scheduler so the system can prioritize or de-prioritize solar thermal relative to other loads.

## 6. Minimal Viable BOM (reproducible starting point)
- 2–4 m² selective flat-plate or evacuated-tube collector
- 150–300 L insulated storage tank with heat-exchanger coil (or direct if open system)
- 18–22 mm copper or PEX piping + insulation
- Tempering valve (anti-scald)
- Pressure & temperature relief valves
- Optional: small differential controller + two sensors
- Optional backup: PV-powered micro-pump

## Status
Detailed sizing, freeze, and stagnation guidance complete. Next: climate-specific example calculations and sensor wiring diagrams.
