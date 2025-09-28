"""
Configuration management utilities
"""

import yaml
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration management class"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "configs/training_config.yaml"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'data': {
                'dataset': 'custom_b2b',
                'batch_size': 1024,
                'validation_split': 0.2
            },
            'models': {
                'neural_collaborative': {'enabled': True},
                'content_based': {'enabled': True},
                'collaborative_filtering': {'enabled': True},
                'hybrid': {'enabled': True}
            },
            'training': {
                'save_models': True,
                'model_dir': 'models/checkpoints',
                'evaluate_models': True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """Save configuration to file"""
        save_path = path or self.config_path
        
        with open(save_path, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
        
        logger.info(f"Configuration saved to {save_path}")
