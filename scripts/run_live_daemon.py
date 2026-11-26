import os
import sys
import time
import argparse
import signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapt.telemetry.linux_collector import LinuxTelemetryCollector
from adapt.telemetry.buffer import SlidingBuffer
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.forecasting.confidence import ConfidenceEstimator
from adapt.policy.policy_engine import PolicyEngine
from adapt.policy.safety_guard import SafetyGuard
from adapt.policy.drift_detector import ConceptDriftDetector
from adapt.policy.hysteresis import HysteresisController
from adapt.actuator.cgroups_v2 import CgroupsV2Actuator
from adapt.utils.logger import get_logger

logger = get_logger("live_daemon")
running = True

def handle_sigint(sig, frame):
    global running
    logger.info("Termination signal received. Exiting daemon safely.")
    running = False

signal.signal(signal.SIGINT, handle_sigint)

def main():
    parser = argparse.ArgumentParser(description="Run Live User-Space Adapt Daemon")
    parser.add_argument("--interval", type=float, default=1.0, help="Epoch interval (seconds)")
    parser.add_argument("--dry_run", action="store_true", default=True, help="Safe dry-run mode")
    parser.add_argument("--max_epochs", type=int, default=10, help="Max run cycles (0=forever)")
    args = parser.parse_args()

    collector = LinuxTelemetryCollector(sample_interval=0.1)
    buffer = SlidingBuffer(capacity=8)
    forecaster = MovingAverageForecaster(horizon=3)
    confidence_engine = ConfidenceEstimator(window_size=8)
    policy = PolicyEngine()
    safety = SafetyGuard()
    drift = ConceptDriftDetector()
    hysteresis = HysteresisController()
    actuator = CgroupsV2Actuator(dry_run=args.dry_run)

    logger.info(f"Adapt Live Daemon initialized. Dry-run: {args.dry_run}. Interval: {args.interval}s")
    
    epoch = 0
    current_quota = 50.0
    last_pred = None
    prev_cpu = None

    while running:
        epoch += 1
        telemetry = collector.sample()
        cpu = telemetry["cpu_utilization"]
        buffer.append(cpu)

        if last_pred is not None:
            confidence_engine.record_outcome(last_pred, cpu, prev_cpu)
            drift.update(last_pred, cpu)
            
        prev_cpu = cpu

        if buffer.is_ready():
            window = buffer.get_window()
            pred = forecaster.predict(window)
            last_pred = pred
            
            # Connected real confidence engine (not permanent 1.0 placeholder)
            conf = confidence_engine.get_confidence()
            is_drift = drift.drift_detected
            
            is_safe, reason = safety.evaluate(
                predicted_cpu=pred,
                confidence=conf,
                drift_detected=is_drift,
                inference_latency_ms=forecaster.last_inference_latency_ms
            )

            if is_safe:
                pol = policy.decide_allocation(cpu, pred, current_quota)
                target = pol["target_quota"]
                if hysteresis.should_apply_change(target, current_quota, pol["is_critical"]):
                    current_quota = target
                    actuator.set_cpu_quota(current_quota)
                    logger.info(f"[EPOCH {epoch}] CPU={cpu:.1f}% FORECAST={pred:.1f}% CONF={conf:.2f} POLICY={pol['decision']} QUOTA={current_quota:.1f}%")
                else:
                    logger.info(f"[EPOCH {epoch}] CPU={cpu:.1f}% FORECAST={pred:.1f}% CONF={conf:.2f} [HYSTERESIS BLOCKED]")
            else:
                logger.warning(f"[EPOCH {epoch}] SAFETY TRIGGERED: {reason} (Conf={conf:.2f}) -> FALLBACK BASELINE")
                actuator.reset()
        else:
            logger.info(f"[EPOCH {epoch}] Warming sliding buffer ({len(buffer.buffer)}/{buffer.capacity}) CPU={cpu:.1f}%")

        if args.max_epochs > 0 and epoch >= args.max_epochs:
            break

        time.sleep(args.interval)

    logger.info("Daemon gracefully stopped.")

if __name__ == "__main__":
    main()
