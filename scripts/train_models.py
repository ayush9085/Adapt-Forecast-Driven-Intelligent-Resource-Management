import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import sys

import argparse
import json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapt.datasets.synthetic import generate_synthetic_workload
from adapt.datasets.sliding_window import create_sliding_windows, train_val_test_split_chronological
from adapt.forecasting.svr_model import SVRForecaster
from adapt.forecasting.rf_model import RandomForestForecaster
from adapt.forecasting.xgboost_model import XGBoostForecaster
from adapt.forecasting.lstm_model import LSTMForecaster
from adapt.forecasting.gru_model import GRUForecaster
from adapt.forecasting.moving_average import MovingAverageForecaster
from adapt.evaluation.metrics import evaluate_forecast
from adapt.evaluation.explainability import ModelExplainabilityAnalyzer

FEATURE_COLS = ["cpu_utilization", "memory_utilization", "io_rate", "task_count", "request_rate"]

def main():
    parser = argparse.ArgumentParser(description="Train and benchmark 5 standard time-series ML algorithms")
    parser.add_argument("--duration", type=int, default=300, help="Training trace duration")
    parser.add_argument("--epochs", type=int, default=20, help="Epochs for neural models")
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
    
    train_cpu = train_df["cpu_utilization"].values
    test_cpu = test_df["cpu_utilization"].values
    
    train_feats = train_df[FEATURE_COLS].values
    val_feats = val_df[FEATURE_COLS].values
    test_feats = test_df[FEATURE_COLS].values
    
    X_train, y_train = create_sliding_windows(train_feats, train_cpu, args.window_size, args.horizon)
    X_val, y_val = create_sliding_windows(val_feats, val_df["cpu_utilization"].values, args.window_size, args.horizon)
    X_test, y_test = create_sliding_windows(test_feats, test_cpu, args.window_size, args.horizon)

    # 5 Standard Time-Series Comparison Algorithms + Proposed Hybrid Adapt Forecaster
    models = {
        "1. Support Vector Regression (SVR)": SVRForecaster(horizon=args.horizon),
        "2. Random Forest": RandomForestForecaster(horizon=args.horizon, n_estimators=60),
        "3. XGBoost": XGBoostForecaster(horizon=args.horizon, n_estimators=60),
        "4. LSTM": LSTMForecaster(horizon=args.horizon, input_dim=len(FEATURE_COLS), epochs=args.epochs),
        "5. GRU": GRUForecaster(horizon=args.horizon, input_dim=len(FEATURE_COLS), epochs=args.epochs),
        "Proposed Adapt (Statistical-Guided Forecaster)": MovingAverageForecaster(horizon=args.horizon)
    }
    
    eval_results = []
    
    for name, m in models.items():
        print(f"\nTraining & evaluating {name}...")
        if isinstance(m, (LSTMForecaster, GRUForecaster)):
            m.fit(X_train, y_train, val_data=(X_val, y_val))
        elif isinstance(m, (MovingAverageForecaster,)):
            # Moving average uses univariate CPU
            m.fit(X_train[:, :, 0], y_train)
        else:
            m.fit(X_train, y_train)
            
        preds = []
        for i in range(len(X_test)):
            sample = X_test[i] if not isinstance(m, MovingAverageForecaster) else X_test[i, :, 0]
            preds.append(m.predict(sample))
            
        metrics = evaluate_forecast(y_test, preds)
        metrics["model"] = name
        metrics["inference_latency_ms"] = m.last_inference_latency_ms
        eval_results.append(metrics)
        print(f"Results for {name}: MAE={metrics['mae']}, RMSE={metrics['rmse']}, DirAcc={metrics['directional_accuracy']}%, Latency={metrics['inference_latency_ms']:.3f}ms")

    results_df = pd.DataFrame(eval_results)
    
    # Explainability on XGBoost
    xgb_forecaster = models["3. XGBoost"]
    xai = ModelExplainabilityAnalyzer(feature_names=FEATURE_COLS)
    shap_summary = xai.compute_shap_summary(xgb_forecaster, X_test)
    
    metadata = {
        "results": eval_results,
        "best_rmse_model": results_df.loc[results_df["rmse"].idxmin()]["model"],
        "best_mae_model": results_df.loc[results_df["mae"].idxmin()]["model"],
        "fastest_model": results_df.loc[results_df["inference_latency_ms"].idxmin()]["model"],
        "best_directional_accuracy_model": results_df.loc[results_df["directional_accuracy"].idxmax()]["model"],
        "xai_shap_summary": shap_summary,
        "feature_cols": FEATURE_COLS,
        "window_size": args.window_size,
        "horizon": args.horizon
    }
    
    meta_path = "models/metadata/model_comparison.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\n[✓] Standard 5-model comparison and XAI results saved to {meta_path}")
    print(results_df[["model", "mae", "rmse", "directional_accuracy", "inference_latency_ms"]].to_string(index=False))

if __name__ == "__main__":
    main()
