import os
import torch
import torch.nn as nn
import numpy as np
from typing import Optional, Dict, Any, Tuple
from adapt.forecasting.base import BaseForecaster
from sklearn.preprocessing import StandardScaler

class _LSTMNetwork(nn.Module):
    def __init__(self, input_dim: int = 1, hidden_dim: int = 32, num_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out.squeeze(-1)

class LSTMForecaster(BaseForecaster):
    """
    Model 5: Deep Long Short-Term Memory (LSTM) Recurrent Neural Network.
    Supports multivariate input tensors [samples, timesteps, features].
    Includes validation loss tracking, early stopping, and checkpoint restoration.
    """
    def __init__(
        self,
        horizon: int = 3,
        input_dim: int = 1,
        hidden_dim: int = 32,
        num_layers: int = 1,
        epochs: int = 30,
        lr: float = 0.005,
        patience: int = 6
    ):
        super().__init__(name="LSTM", horizon=horizon)
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.epochs = epochs
        self.lr = lr
        self.patience = patience
        self.model: Optional[_LSTMNetwork] = None
        self.scaler = StandardScaler()
        self.target_scaler = StandardScaler()
        self.training_history = []
        self.validation_history = []
        self.best_epoch = 0

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        val_data: Optional[Tuple[np.ndarray, np.ndarray]] = None
    ) -> "LSTMForecaster":
        if X.ndim == 2:
            X = np.expand_dims(X, -1)
            
        samples, seq_len, feats = X.shape
        self.input_dim = feats
        
        # Fit scalers STRICTLY on training data (no leakage)
        X_flat = X.reshape(-1, feats)
        self.scaler.fit(X_flat)
        X_scaled = self.scaler.transform(X_flat).reshape(samples, seq_len, feats)
        y_scaled = self.target_scaler.fit_transform(y.reshape(-1, 1)).flatten()
        
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        y_tensor = torch.tensor(y_scaled, dtype=torch.float32)
        
        # Optional validation data
        has_val = False
        if val_data is not None:
            X_val, y_val = val_data
            if X_val.ndim == 2:
                X_val = np.expand_dims(X_val, -1)
            v_samples, v_seq, v_feats = X_val.shape
            X_val_flat = X_val.reshape(-1, v_feats)
            X_val_scaled = self.scaler.transform(X_val_flat).reshape(v_samples, v_seq, v_feats)
            y_val_scaled = self.target_scaler.transform(y_val.reshape(-1, 1)).flatten()
            X_val_tensor = torch.tensor(X_val_scaled, dtype=torch.float32)
            y_val_tensor = torch.tensor(y_val_scaled, dtype=torch.float32)
            has_val = True

        self.model = _LSTMNetwork(self.input_dim, self.hidden_dim, self.num_layers)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        criterion = nn.MSELoss()
        
        best_val_loss = float("inf")
        best_state = None
        patience_counter = 0
        
        self.training_history = []
        self.validation_history = []
        
        for epoch in range(self.epochs):
            self.model.train()
            optimizer.zero_grad()
            preds = self.model(X_tensor)
            loss = criterion(preds, y_tensor)
            loss.backward()
            optimizer.step()
            train_loss = float(loss.item())
            self.training_history.append(train_loss)
            
            if has_val:
                self.model.eval()
                with torch.no_grad():
                    v_preds = self.model(X_val_tensor)
                    val_loss = float(criterion(v_preds, y_val_tensor).item())
                    self.validation_history.append(val_loss)
                    
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                    self.best_epoch = epoch
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        break
                        
        if best_state is not None:
            self.model.load_state_dict(best_state)
            
        self.is_fitted = True
        return self

    def _predict_raw(self, window: np.ndarray) -> float:
        if not self.is_fitted or self.model is None:
            return float(window[-1, 0] if window.ndim == 2 else window[-1])
            
        if window.ndim == 1:
            window = np.expand_dims(window, -1)
            
        # Match expected features dimension
        if window.shape[-1] < self.input_dim:
            # Pad with zeros if single univariate was passed
            pad_width = self.input_dim - window.shape[-1]
            window = np.pad(window, ((0, 0), (0, pad_width)), mode="edge")
        elif window.shape[-1] > self.input_dim:
            window = window[:, :self.input_dim]
            
        w_scaled = self.scaler.transform(window)
        w_tensor = torch.tensor(w_scaled, dtype=torch.float32).unsqueeze(0)
        
        self.model.eval()
        with torch.no_grad():
            pred_scaled = self.model(w_tensor).item()
            pred = self.target_scaler.inverse_transform([[pred_scaled]])[0, 0]
            
        return float(pred)

    def save(self, filepath: str):
        if self.model is not None:
            torch.save({
                "model_state": self.model.state_dict(),
                "scaler": self.scaler,
                "target_scaler": self.target_scaler,
                "input_dim": self.input_dim,
                "hidden_dim": self.hidden_dim,
                "num_layers": self.num_layers,
                "horizon": self.horizon,
                "best_epoch": self.best_epoch
            }, filepath)

    def load(self, filepath: str):
        checkpoint = torch.load(filepath, weights_only=False)
        self.input_dim = checkpoint["input_dim"]
        self.hidden_dim = checkpoint["hidden_dim"]
        self.num_layers = checkpoint["num_layers"]
        self.horizon = checkpoint["horizon"]
        self.scaler = checkpoint["scaler"]
        self.target_scaler = checkpoint["target_scaler"]
        self.best_epoch = checkpoint.get("best_epoch", 0)
        
        self.model = _LSTMNetwork(self.input_dim, self.hidden_dim, self.num_layers)
        self.model.load_state_dict(checkpoint["model_state"])
        self.model.eval()
        self.is_fitted = True
