# Generator 03 — Thermoelectric + PV Hybrid Heat-Pump Assist — Components & Control

**Dyad process:** Lumen expanded efficient low-power heating architectures and residual-heat recovery. Aegis constrained power budgets, realistic COP expectations, and tight integration with existing energy-aware code.

## 1. Recommended Component Classes

| Function | Suggested Class | Notes |
|----------|-----------------|-------|
| PV array | 100–400 W (sized to load + margin) | Match to local insolation and daily hot-water energy need |
| Storage | LiFePO₄ 12/24 V or large supercapacitor bank | Prefer chemistry with long cycle life |
| Charge controller | MPPT, low quiescent current | Essential for efficiency |
| Heating element | Low-power DC heat-pump (mini) or high-quality thermoelectric modules | Heat-pump preferred for COP > 1; TECs for simplicity / residual heat |
| Circulation | 12 V DC brushless pump, 5–20 W | Only run when needed |
| Controller | ESP32-C3 or ESP32-S3 | Runs energy-aware policy |
| Sensors | DS18B20 or equivalent (water, ambient), voltage/current on PV and storage | Feed the scheduler |
| Optional TEG | Bismuth-telluride modules on residual heat sources | Trickle contribution to storage |

## 2. Power Budget Reality Check (Aegis)
- Pure resistive 1 kW heater is rarely viable on small off-grid PV.
- Target: heat-pump or staged system whose average electrical draw is compatible with the available PV + storage.
- Example target: 100–300 W electrical input for useful thermal output via COP 2–4 under favorable conditions.
- Always measure real COP and standby consumption.

## 3. Control Code Sketch (Python / MicroPython compatible)

```python
# Sketch only — integrate with energy_aware_scheduler.py concepts

class HybridWaterHeaterPolicy:
    def __init__(self, v_min=11.5, v_high=13.2, tank_target=50.0, tank_max=60.0):
        self.v_min = v_min
        self.v_high = v_high
        self.tank_target = tank_target
        self.tank_max = tank_max

    def decide(self, storage_v, tank_c, solar_w, residual_heat_available):
        if tank_c >= self.tank_max:
            return "OFF_HEAT_DUMP_OR_IDLE"
        if storage_v < self.v_min:
            return "OFF_PROTECT_STORAGE"
        if tank_c >= self.tank_target and solar_w < 50:
            return "OFF_OR_MAINTAIN"
        if storage_v >= self.v_high and tank_c < self.tank_target:
            return "RUN_HEAT_PUMP_OR_TEC"
        if residual_heat_available and storage_v < self.v_high:
            return "ENABLE_TEG_HARVEST"
        return "STANDBY_MONITOR"
```

This policy is intentionally simple and auditable. It can be replaced later by a quantized RL policy from the model database.

## 4. Integration Points
- Storage voltage and estimated joules already used by the energy-harvester-tinyml scheduler.
- Tank temperature becomes an additional priority signal for the Operator AI Machinery.
- Residual-heat TEGs feed the same storage bus when possible.

## 5. Status
Component classes and a concrete, testable control sketch are defined. Next physical step: select specific modules, measure real power and COP, and close the loop with the existing energy-aware code.
