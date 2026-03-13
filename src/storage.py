import json
import os
from pathlib import Path
from typing import Set

class HistoryStore:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_history_file(self, config_file_name: str) -> Path:
        # e.g., config/jane_doe.json -> data/jane_doe.history.json
        base_name = config_file_name.replace(".json", "")
        return self.data_dir / f"{base_name}.history.json"
    
    def load_history(self, config_file_name: str) -> Set[str]:
        history_file = self._get_history_file(config_file_name)
        if not history_file.exists():
            return set()
        
        try:
            with open(history_file, 'r') as f:
                return set(json.load(f))
        except Exception:
            return set()
    
    def save_history(self, config_file_name: str, history: Set[str]):
        history_file = self._get_history_file(config_file_name)
        try:
            with open(history_file, 'w') as f:
                json.dump(list(history), f)
        except Exception as e:
            print(f"Error saving history for {config_file_name}: {e}")
