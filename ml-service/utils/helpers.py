"""
Helper utilities
"""

import os
import json
import pickle
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class Helpers:
    """Helper utility functions"""
    
    @staticmethod
    def ensure_directory(path: str):
        """Ensure directory exists"""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def save_json(data: Any, filepath: str):
        """Save data as JSON"""
        Helpers.ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data saved to {filepath}")
    
    @staticmethod
    def load_json(filepath: str) -> Optional[Dict]:
        """Load data from JSON"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"File not found: {filepath}")
            return None
    
    @staticmethod
    def save_pickle(data: Any, filepath: str):
        """Save data as pickle"""
        Helpers.ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"Data saved to {filepath}")
    
    @staticmethod
    def load_pickle(filepath: str) -> Optional[Any]:
        """Load data from pickle"""
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            logger.warning(f"File not found: {filepath}")
            return None
    
    @staticmethod
    def format_number(num: float, decimals: int = 4) -> str:
        """Format number with specified decimal places"""
        return f"{num:.{decimals}f}"
    
    @staticmethod
    def format_percentage(num: float, decimals: int = 2) -> str:
        """Format number as percentage"""
        return f"{num * 100:.{decimals}f}%"
    
    @staticmethod
    def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
        """Split list into chunks"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        """Safely divide two numbers"""
        return numerator / denominator if denominator != 0 else default
