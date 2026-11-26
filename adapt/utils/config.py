import os
import yaml
from typing import Any, Dict

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.yaml")

def load_config(config_path: str = None) -> Dict[str, Any]:
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def get_subconfig(key: str, default: Any = None, config_path: str = None) -> Any:
    cfg = load_config(config_path)
    return cfg.get(key, default)
