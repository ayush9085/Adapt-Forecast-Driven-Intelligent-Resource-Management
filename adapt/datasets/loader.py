import os
import io
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, Tuple
from adapt.datasets.synthetic import generate_synthetic_workload

REQUIRED_COLUMNS = [
    "timestamp", "cpu_utilization"
]

RECOMMENDED_COLUMNS = [
    "memory_utilization", "io_rate", "task_count", "request_rate", "latency_ms"
]

def validate_and_normalize_trace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates trace schema, chronologically sorts, handles NaNs, and provides standard defaults.
    """
    df = df.copy()
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Trace CSV is missing required column: '{col}'")
            
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    
    # Impute missing values linearly
    df["cpu_utilization"] = df["cpu_utilization"].interpolate(method="linear").bfill().ffill()
    df["cpu_utilization"] = np.clip(df["cpu_utilization"], 0.0, 100.0)
    
    for col in RECOMMENDED_COLUMNS:
        if col not in df.columns:
            if col == "memory_utilization":
                df[col] = 40.0 + 0.3 * df["cpu_utilization"]
            elif col == "io_rate":
                df[col] = 50.0 + 1.5 * df["cpu_utilization"]
            elif col == "task_count":
                df[col] = 10 + (df["cpu_utilization"] // 10).astype(int)
            elif col == "request_rate":
                df[col] = 100.0 + 10.0 * df["cpu_utilization"]
            elif col == "latency_ms":
                df[col] = 5.0 + 0.1 * df["cpu_utilization"]
        else:
            df[col] = df[col].interpolate(method="linear").bfill().ffill()
            
    if "tenant_id" not in df.columns:
        df["tenant_id"] = "default_tenant"
        
    return df

def load_csv_trace(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Trace file not found: {filepath}")
    df = pd.read_csv(filepath)
    return validate_and_normalize_trace(df)

def load_alibaba_or_azure_trace_adapter(
    filepath: str,
    trace_type: str = "alibaba"
) -> pd.DataFrame:
    """
    Adapter for external public cloud traces (Alibaba Cluster Trace / Azure VM traces).
    Converts raw cloud trace formats into Adapt standard telemetry format.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Public cloud trace not found at {filepath}. "
            f"Please download the {trace_type} dataset and place it in data/raw/"
        )
    raw_df = pd.read_csv(filepath)
    
    if trace_type.lower() == "alibaba":
        # Alibaba trace typical columns: time_stamp, cpu_util_percent, mem_util_percent
        time_col = [c for c in raw_df.columns if "time" in c.lower()][0]
        cpu_col = [c for c in raw_df.columns if "cpu" in c.lower()][0]
        df = pd.DataFrame({
            "timestamp": np.arange(len(raw_df)),
            "cpu_utilization": raw_df[cpu_col] if raw_df[cpu_col].max() <= 100.0 else raw_df[cpu_col] / 100.0,
            "tenant_id": "alibaba_workload"
        })
    elif trace_type.lower() == "azure":
        time_col = [c for c in raw_df.columns if "time" in c.lower()][0]
        cpu_col = [c for c in raw_df.columns if "cpu" in c.lower()][0]
        df = pd.DataFrame({
            "timestamp": np.arange(len(raw_df)),
            "cpu_utilization": raw_df[cpu_col],
            "tenant_id": "azure_vm_workload"
        })
    else:
        df = raw_df
        
    return validate_and_normalize_trace(df)
