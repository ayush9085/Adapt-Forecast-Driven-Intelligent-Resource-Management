import os
import sys
import argparse
import json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapt.datasets.synthetic import generate_synthetic_workload
from adapt.datasets.sliding_window import create_sliding_windows, train_val_test_split_chronological
from adapt.forecasting.naive import NaivePersistenceForecaster
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.forecasting.exponential_smoothing import ExponentialSmoothingForecaster
from adapt.forecasting.arima_model import ARIMAForecaster
from adapt.forecasting.lstm_model import LSTMForecaster
from adapt.forecasting.gru_model import GRUForecaster
from adapt.evaluation.metrics import evaluate_forecast

FEATURE_COLS = ["cpu_utilization", "memory_utilization", "io_rate", "task_count", "request_rate"]

def main():
    parser = argparse.ArgumentParser(description="Train and evaluate forecasting models")
    parser.add_argument("--duration", type=int, default=300, help="Training trace duration")
    parser.add_argument("--epochs", type=int, default=25, help="Epochs for neural models")
    parser.add_argument("--horizon", type=int, default=3, help="Prediction horizon")
    parser.add_argument("--window_size", type=int, default=12, help="Sliding window size")
    parser.add_argument("--output_dir", type=str, default="models/checkpoints", help="Save directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs("models/metadata", exist_ok=True)
    
    print(f"Generating training telemetry ({args.duration} epochs)...")
    df = generate_synthetic_workload(duration_seconds=args.duration, seed=42)
    
    train_df, val_df, test_df = train_val_test_split_chronological(df, train_ratio=0.7, val_ratio=0.15)
    print(f"Split sizes: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)} (Chronological, No Leakage)")
    
    # Univariate CPU
    train_cpu = train_df["cpu_utilization"].values
    test_cpu = test_df["cpu_utilization"].values
    
    X_train_uni, y_train_uni = create_sliding_windows(train_cpu, train_cpu, args.window_size, args.horizon)
    X_test_uni, y_test_uni = create_sliding_windows(test_cpu, test_cpu, args.window_size, args.horizon)
    
    # Multivariate features for neural models
    train_feats = train_df[FEATURE_COLS].values
    val_feats = val_df[FEATURE_COLS].values
    test_feats = test_df[FEATURE_COLS].values
    
    X_train_multi, y_train_multi = create_sliding_windows(train_feats, train_cpu, args.window_size, args.horizon)
    X_val_multi, y_val_multi = create_sliding_windows(val_feats, val_df["cpu_utilization"].values, args.window_size, args.horizon)
    X_test_multi, y_test_multi = create_sliding_windows(test_feats, test_cpu, args.window_size, args.horizon)

    models = {
        "NaivePersistence": (NaivePersistenceForecaster(horizon=args.horizon), False),
        "MovingAverage": (MovingAverageForecaster(horizon=args.horizon), False),
        "ExponentialSmoothing": (ExponentialSmoothingForecaster(horizon=args.horizon), False),
        "ARIMA": (ARIMAForecaster(horizon=args.horizon), False),
        "LSTM": (LSTMForecaster(horizon=args.horizon, input_dim=len(FEATURE_COLS), epochs=args.epochs), True),
        "GRU": (GRUForecaster(horizon=args.horizon, input_dim=len(FEATURE_COLS), epochs=args.epochs), True)
    }
    
    eval_results = []
    
    for name, (m, is_multi) in models.items():
        print(f"\nTraining & evaluating {name} (Multivariate: {is_multi})...")
        if is_multi:
            m.fit(X_train_multi, y_train_multi, val_data=(X_val_multi, y_val_multi))
            test_X, test_y = X_test_multi, y_test_multi
        else:
            m.fit(X_train_uni, y_train_uni)
            test_X, test_y = X_test_uni, y_test_uni
            
        preds = []
        for i in range(len(test_X)):
            preds.append(m.predict(test_X[i]))
            
        metrics = evaluate_forecast(test_y, preds)
        metrics["model"] = name
        metrics["inference_latency_ms"] = m.last_inference_latency_ms
        metrics["is_multivariate"] = is_multi
        eval_results.append(metrics)
        print(f"Results for {name}: MAE={metrics['mae']}, RMSE={metrics['rmse']}, DirAcc={metrics['directional_accuracy']}%, Latency={metrics['inference_latency_ms']:.2f}ms")
        
        if hasattr(m, "save"):
            ckpt = os.path.join(args.output_dir, f"{name.lower()}_model.pt")
            m.save(ckpt)
            print(f"Saved checkpoint: {ckpt}")

    results_df = pd.DataFrame(eval_results)
    
    # Determine best models dynamically based on empirical measurement
    best_rmse_model = results_df.loc[results_df["rmse"].idxmin()]["model"]
    best_mae_model = results_df.loc[results_df["mae"].idxmin()]["model"]
    fastest_model = results_df.loc[results_df["inference_latency_ms"].idxmin()]["model"]
    best_dir_acc_model = results_df.loc[results_df["directional_accuracy"].idxmax()]["model"]
    
    metadata = {
        "results": eval_results,
        "best_rmse_model": best_rmse_model,
        "best_mae_model": best_mae_model,
        "fastest_model": fastest_model,
        "best_directional_accuracy_model": best_dir_acc_model,
        "feature_cols": FEATURE_COLS,
        "window_size": args.window_size,
        "horizon": args.horizon
    }
    
    meta_path = "models/metadata/model_comparison.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\n[✓] Comparison and dynamic rankings saved to {meta_path}")
    print(results_df[["model", "mae", "rmse", "directional_accuracy", "inference_latency_ms"]].to_string(index=False))

if __name__ == "__main__":
    main()
