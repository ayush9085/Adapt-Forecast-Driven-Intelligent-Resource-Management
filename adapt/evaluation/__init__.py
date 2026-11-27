from adapt.evaluation.metrics import (
    evaluate_forecast,
    calculate_scheduler_metrics,
    calculate_mape_safe,
    calculate_directional_accuracy,
    calculate_control_response_lag
)
from adapt.evaluation.experiments import ExperimentLogger
from adapt.evaluation.explainability import ModelExplainabilityAnalyzer

# Lazy load BenchmarkEngine and AblationStudyEngine to break circular import with SimulationEngine
def __getattr__(name: str):
    if name == "BenchmarkEngine":
        from adapt.evaluation.benchmark import BenchmarkEngine
        return BenchmarkEngine
    elif name == "AblationStudyEngine":
        from adapt.evaluation.ablation import AblationStudyEngine
        return AblationStudyEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "evaluate_forecast",
    "calculate_scheduler_metrics",
    "calculate_mape_safe",
    "calculate_directional_accuracy",
    "calculate_control_response_lag",
    "ExperimentLogger",
    "BenchmarkEngine",
    "ModelExplainabilityAnalyzer",
    "AblationStudyEngine"
]

