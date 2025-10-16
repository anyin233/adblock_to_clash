"""Configuration file parser for rule converter."""
import yaml
from typing import List, Dict, Any
from pathlib import Path


class Config:
    """Configuration parser and validator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize config parser.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.rules: List[str] = []
        self.target: str = ""
        
    def load(self) -> None:
        """Load and parse configuration file.
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config format is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        self._validate(data)
        self.rules = data['rules']
        self.target = data['target']
    
    def _validate(self, data: Dict[str, Any]) -> None:
        """Validate configuration data.
        
        Args:
            data: Parsed YAML data
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not isinstance(data, dict):
            raise ValueError("Config must be a dictionary")
        
        if 'rules' not in data:
            raise ValueError("Missing 'rules' field in config")
        
        if 'target' not in data:
            raise ValueError("Missing 'target' field in config")
        
        if not isinstance(data['rules'], list):
            raise ValueError("'rules' must be a list")
        
        if not data['rules']:
            raise ValueError("'rules' list cannot be empty")
        
        if data['target'] != 'clash':
            raise ValueError(f"Unsupported target: {data['target']}. Only 'clash' is supported")
