import os
import sys
import argparse
import pandas as pd

# Add repo to pythonpath
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapt.datasets.synthetic import generate_synthetic_workload, generate_multi_tenant_workloads
from adapt.simulation.scenarios import get_scenario

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic workload traces for Adapt")
    parser.add_argument("--duration", type=int, default=120, help="Duration in ticks (seconds)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output_dir", type=str, default="data/synthetic", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    
    # 1. Base synthetic workload
    base_df = generate_synthetic_workload(duration_seconds=args.duration, seed=args.seed)
    base_path = os.path.join(args.output_dir, "synthetic_workload.csv")
    base_df.to_csv(base_path, index=False)
    print(f"[✓] Saved base synthetic workload: {base_path} ({len(base_df)} rows)")

    # 2. Multi-tenant workload set
    mt_dict = generate_multi_tenant_workloads(duration_seconds=args.duration, seed=args.seed)
    for name, df in mt_dict.items():
        p = os.path.join(args.output_dir, f"{name}.csv")
        df.to_csv(p, index=False)
        print(f"[✓] Saved multi-tenant trace: {p}")

    # 3. Standard scenario library
    scenarios = ["Stable Load", "Step Contention", "Periodic / Diurnal", "Bursty Traffic", "Concept Drift", "Presentation Demo"]
    for sc in scenarios:
        sc_df = get_scenario(sc, duration=args.duration, seed=args.seed)
        clean_name = sc.lower().replace(" ", "_").replace("/", "_")
        sc_path = os.path.join(args.output_dir, f"scenario_{clean_name}.csv")
        sc_df.to_csv(sc_path, index=False)
        print(f"[✓] Saved scenario: {sc_path}")

    print("\nAll synthetic workload traces generated successfully!")

if __name__ == "__main__":
    main()
