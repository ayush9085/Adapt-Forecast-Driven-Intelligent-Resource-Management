import pandas as pd
from typing import Dict, Any, List
from adapt.simulation.simulator import SimulationEngine
from adapt.simulation.scenarios import get_scenario
from adapt.scheduler.adapt_scheduler import AdaptScheduler
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.policy.policy_engine import PolicyEngine
from adapt.policy.safety_guard import SafetyGuard
from adapt.policy.drift_detector import ConceptDriftDetector
from adapt.policy.hysteresis import HysteresisController

class AblationStudyEngine:
    """
    Component Ablation Study for Adapt Framework.
    Removes one proposed architectural component at a time to isolate individual contributions:
    1. Full Adapt (All components: Forecast + Safety + Drift + Hysteresis)
    2. Adapt without Hysteresis (Disabled anti-oscillation cooldown)
    3. Adapt without Safety Guard (No confidence/drift fallback)
    4. Adapt without Proactive Headroom (Headroom factor = 1.0)
    5. Pure Reactive Baseline (No predictive forecaster)
    """
    def __init__(self, simulation_engine: SimulationEngine = None):
        self.sim = simulation_engine or SimulationEngine()

    def run_ablation(self, scenario_name: str = "Presentation Demo", duration: int = 100) -> pd.DataFrame:
        workload_df = get_scenario(scenario_name, duration=duration)
        forecaster = MovingAverageForecaster(horizon=3)
        
        configs = {
            "1. Full Adapt (Proposed)": AdaptScheduler(
                forecaster=forecaster,
                policy_engine=PolicyEngine(headroom_factor=1.15),
                safety_guard=SafetyGuard(enabled=True),
                drift_detector=ConceptDriftDetector(),
                hysteresis=HysteresisController(cooldown_ticks=3, minimum_change=8.0)
            ),
            "2. Adapt w/o Hysteresis": AdaptScheduler(
                forecaster=forecaster,
                policy_engine=PolicyEngine(headroom_factor=1.15),
                safety_guard=SafetyGuard(enabled=True),
                drift_detector=ConceptDriftDetector(),
                hysteresis=HysteresisController(cooldown_ticks=0, minimum_change=0.0) # Disabled
            ),
            "3. Adapt w/o Safety Guard": AdaptScheduler(
                forecaster=forecaster,
                policy_engine=PolicyEngine(headroom_factor=1.15),
                safety_guard=SafetyGuard(enabled=False), # Disabled
                drift_detector=None,
                hysteresis=HysteresisController(cooldown_ticks=3, minimum_change=8.0)
            ),
            "4. Adapt w/o Proactive Headroom": AdaptScheduler(
                forecaster=forecaster,
                policy_engine=PolicyEngine(headroom_factor=1.0), # No headroom buffer
                safety_guard=SafetyGuard(enabled=True),
                drift_detector=ConceptDriftDetector(),
                hysteresis=HysteresisController(cooldown_ticks=3, minimum_change=8.0)
            )
        }
        
        rows = []
        for name, sched in configs.items():
            res = self.sim.run(sched, workload_df.copy())
            m = res["metrics"]
            rows.append({
                "Configuration": name,
                "Avg Latency (ms)": m["avg_latency"],
                "P95 Latency (ms)": m["p95_latency"],
                "P99 Latency (ms)": m["p99_latency"],
                "SLA Violations": m["sla_violations"],
                "Throttled Time (s)": m["total_throttled_sec"],
                "Resource Efficiency (%)": m["resource_efficiency"],
                "Allocation Changes (Thrash)": m["allocation_changes"]
            })
            
        return pd.DataFrame(rows)
