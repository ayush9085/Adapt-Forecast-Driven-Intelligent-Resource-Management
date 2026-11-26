import numpy as np
import pandas as pd
from typing import Tuple, List, Optional

def create_sliding_windows(
    data: np.ndarray,
    target: np.ndarray,
    window_size: int = 12,
    horizon: int = 3
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates strictly chronological supervised sliding windows without lookahead leakage.
    X shape: [samples, window_size, num_features]
    y shape: [samples] (predicting target at t + horizon - 1)
    """
    X, y = [], []
    num_samples = len(data)
    
    # Needs window_size past samples + horizon future
    for i in range(num_samples - window_size - horizon + 1):
        window = data[i : i + window_size]
        target_val = target[i + window_size + horizon - 1]
        X.append(window)
        y.append(target_val)
        
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

def train_val_test_split_chronological(
    df: pd.DataFrame,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Strict chronological split - NO shuffling to avoid temporal data leakage.
    """
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()
    
    return train_df, val_df, test_df
