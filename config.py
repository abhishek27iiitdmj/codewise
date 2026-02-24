"""
Configuration management for AI Code Review Bot
"""

import yaml
from typing import Dict
from utils import logger


class Config:
    """Configuration loader"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_path} not found, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 2000,
            'temperature': 0.2,
            'max_diff_size': 5000,
            'max_files': 50,
            'exclude_patterns': ['vendor/**', 'node_modules/**', 'storage/**', '*.lock'],
            'skip_large_prs': True,
            'post_warning_on_skip': True,
            'enable_cost_tracking': True
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
