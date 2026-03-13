import json
import os
from pathlib import Path
from typing import List, Dict

def load_configs(config_dir: str = "config") -> List[Dict]:
    configs = []
    config_path = Path(config_dir)
    if not config_path.exists():
        return configs
    
    for config_file in config_path.glob("*.json"):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                config['file_name'] = config_file.name
                configs.append(config)
        except Exception as e:
            print(f"Error loading {config_file}: {e}")
    
    return configs
