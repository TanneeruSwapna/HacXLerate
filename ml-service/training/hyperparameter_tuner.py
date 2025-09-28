"""
Hyperparameter tuning utilities
"""

import itertools
import random
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class HyperparameterTuner:
    """Hyperparameter tuning for ML models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def grid_search(self, param_grid: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Generate grid search parameter combinations"""
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        
        combinations = []
        for combination in itertools.product(*values):
            param_dict = dict(zip(keys, combination))
            combinations.append(param_dict)
        
        logger.info(f"Generated {len(combinations)} parameter combinations")
        return combinations
    
    def random_search(self, param_distributions: Dict[str, List[Any]], 
                     n_iter: int = 50) -> List[Dict[str, Any]]:
        """Generate random search parameter combinations"""
        combinations = []
        
        for _ in range(n_iter):
            param_dict = {}
            for param_name, param_values in param_distributions.items():
                param_dict[param_name] = random.choice(param_values)
            combinations.append(param_dict)
        
        logger.info(f"Generated {len(combinations)} random parameter combinations")
        return combinations
    
    def get_ncf_hyperparameters(self) -> Dict[str, List[Any]]:
        """Get Neural Collaborative Filtering hyperparameters"""
        return {
            'embedding_dim': [32, 50, 64, 100],
            'hidden_layers': [
                [64, 32],
                [128, 64],
                [128, 64, 32],
                [256, 128, 64]
            ],
            'learning_rate': [0.001, 0.005, 0.01],
            'batch_size': [512, 1024, 2048],
            'dropout': [0.1, 0.2, 0.3]
        }
    
    def get_content_based_hyperparameters(self) -> Dict[str, List[Any]]:
        """Get Content-Based hyperparameters"""
        return {
            'similarity_threshold': [0.5, 0.6, 0.7, 0.8],
            'similarity_metric': ['cosine', 'euclidean', 'manhattan']
        }
    
    def get_collaborative_hyperparameters(self) -> Dict[str, List[Any]]:
        """Get Collaborative Filtering hyperparameters"""
        return {
            'similarity_metric': ['cosine', 'pearson', 'jaccard'],
            'min_similarity': [0.1, 0.2, 0.3],
            'max_neighbors': [20, 50, 100]
        }
