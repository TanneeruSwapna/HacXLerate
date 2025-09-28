"""
Cross-validation utilities
"""

import numpy as np
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class CrossValidator:
    """Cross-validation for ML models"""
    
    def __init__(self, n_folds: int = 5):
        self.n_folds = n_folds
    
    def k_fold_split(self, interactions: Dict[int, Dict[int, float]]) -> List[Tuple[Dict, Dict]]:
        """Split data into k folds"""
        user_ids = list(interactions.keys())
        np.random.seed(42)
        np.random.shuffle(user_ids)
        
        fold_size = len(user_ids) // self.n_folds
        folds = []
        
        for i in range(self.n_folds):
            start_idx = i * fold_size
            end_idx = start_idx + fold_size if i < self.n_folds - 1 else len(user_ids)
            
            fold_user_ids = user_ids[start_idx:end_idx]
            
            # Split into train and validation
            train_interactions = {}
            val_interactions = {}
            
            for user_id in user_ids:
                if user_id in fold_user_ids:
                    val_interactions[user_id] = interactions[user_id]
                else:
                    train_interactions[user_id] = interactions[user_id]
            
            folds.append((train_interactions, val_interactions))
        
        logger.info(f"Created {len(folds)} folds")
        return folds
    
    def time_series_split(self, interactions: Dict[int, Dict[int, float]], 
                         time_splits: List[float]) -> List[Tuple[Dict, Dict]]:
        """Split data by time for temporal validation"""
        # This is a simplified version - in practice, you'd use timestamps
        user_ids = list(interactions.keys())
        np.random.seed(42)
        np.random.shuffle(user_ids)
        
        folds = []
        for split in time_splits:
            split_idx = int(len(user_ids) * split)
            
            train_user_ids = user_ids[:split_idx]
            val_user_ids = user_ids[split_idx:]
            
            train_interactions = {uid: interactions[uid] for uid in train_user_ids}
            val_interactions = {uid: interactions[uid] for uid in val_user_ids}
            
            folds.append((train_interactions, val_interactions))
        
        logger.info(f"Created {len(folds)} time-based folds")
        return folds
