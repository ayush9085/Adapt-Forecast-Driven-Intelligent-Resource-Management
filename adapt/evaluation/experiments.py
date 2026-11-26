import os
import json
import pandas as pd
from typing import Dict, Any, List
from adapt.utils.logger import get_logger

logger = get_logger("experiment_logger")

class ExperimentLogger:
    """
    Saves and serializes experiments with configs, timeseries logs, and benchmark reports.
    """
    def __init__(self, base_dir: str = "results/experiments"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_experiment(
        self,
        exp_id: str,
        config: Dict[str, Any],
        scheduler_metrics: Dict[str, Any],
        timeseries_df: pd.DataFrame,
        notes: str = ""
    ) -> str:
        exp_dir = os.path.join(self.base_dir, exp_id)
        os.makedirs(exp_dir, exist_ok=True)
        
        # 1. Config
        with open(os.path.join(exp_dir, "config.json"), "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
            
        # 2. Metrics
        with open(os.path.join(exp_dir, "metrics.json"), "w", encoding="utf-8") as f:
            json.dump(scheduler_metrics, f, indent=2)
            
        # 3. Time-series trace
        csv_path = os.path.join(exp_dir, "timeseries.csv")
        timeseries_df.to_csv(csv_path, index=False)
        
        # 4. Summary report
        summary_md = f"""# Experiment Report: {exp_id}

- **Scenario**: {config.get('scenario', 'Unknown')}
- **Scheduler**: {config.get('scheduler', 'Unknown')}
- **Model**: {config.get('model', 'Unknown')}
- **Notes**: {notes}

## Key Metrics
- **P95 Latency**: {scheduler_metrics.get('p95_latency', 'N/A')} ms
- **P99 Latency**: {scheduler_metrics.get('p99_latency', 'N/A')} ms
- **SLA Violations**: {scheduler_metrics.get('sla_violations', 'N/A')} ({scheduler_metrics.get('sla_violation_rate', 'N/A')}%)
- **Resource Efficiency**: {scheduler_metrics.get('resource_efficiency', 'N/A')}%
- **Total Throttled Time**: {scheduler_metrics.get('total_throttled_sec', 'N/A')} s
- **Allocation Changes**: {scheduler_metrics.get('allocation_changes', 'N/A')}
- **Safety Fallbacks**: {scheduler_metrics.get('fallback_events', 'N/A')}
"""
        with open(os.path.join(exp_dir, "summary.md"), "w", encoding="utf-8") as f:
            f.write(summary_md)
            
        logger.info(f"Experiment saved successfully: {exp_dir}")
        return exp_dir
