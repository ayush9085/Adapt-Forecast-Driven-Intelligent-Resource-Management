import os
import sys
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapt.evaluation.benchmark import BenchmarkEngine
from adapt.simulation.scenarios import get_scenario
from adapt.forecasting.moving_average import MovingAverageForecaster

def main():
    parser = argparse.ArgumentParser(description="Run official benchmark battery suite")
    parser.add_argument("--scenario", type=str, default="ALL", help="Specific scenario or ALL")
    parser.add_argument("--duration", type=int, default=100, help="Duration for single scenario")
    args = parser.parse_args()

    bench = BenchmarkEngine()
    forecaster = MovingAverageForecaster(horizon=3)

    if args.scenario == "ALL":
        print("\n" + "="*85)
        print("RUNNING ADAPT OFFICIAL TEST SUITE (TC-01, TC-02, TC-03, TC-04)")
        print("="*85)
        suite = bench.run_standard_suite(forecaster=forecaster)
        
        for tc_id, out in suite.items():
            print(f"\n--- {tc_id} ---")
            if "summary_table" in out:
                print(out["summary_table"].to_string(index=False))
            else:
                # TC-04 Overhead output
                print(json.dumps(out, indent=2))
        print("\n" + "="*85 + "\n")
    else:
        print(f"Loading scenario '{args.scenario}'...")
        workload_df = get_scenario(args.scenario, duration=args.duration)
        out = bench.run_comparative_benchmark(workload_df, forecaster=forecaster)
        print("\n" + "="*85)
        print(f"BENCHMARK RESULTS: {args.scenario}")
        print("="*85)
        print(out["summary_table"].to_string(index=False))
        print("="*85 + "\n")

if __name__ == "__main__":
    main()
