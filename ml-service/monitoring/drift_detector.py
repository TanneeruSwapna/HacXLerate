"""
Data drift detection utilities
"""

import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """Detect data drift in incoming data"""
    
    def __init__(self, baseline_data: Dict[str, Any]):
        self.baseline_data = baseline_data
        self.baseline_stats = self._calculate_baseline_stats()
    
    def _calculate_baseline_stats(self) -> Dict[str, Any]:
        """Calculate baseline statistics"""
        interactions = self.baseline_data.get('interactions', {})
        
        # Calculate user interaction statistics
        user_interaction_counts = [len(items) for items in interactions.values()]
        item_interaction_counts = {}
        
        for items in interactions.values():
            for item_id in items.keys():
                item_interaction_counts[item_id] = item_interaction_counts.get(item_id, 0) + 1
        
        return {
            'avg_user_interactions': np.mean(user_interaction_counts),
            'std_user_interactions': np.std(user_interaction_counts),
            'total_users': len(interactions),
            'total_items': len(item_interaction_counts),
            'item_popularity_distribution': list(item_interaction_counts.values())
        }
    
    def detect_drift(self, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect drift in current data"""
        current_stats = self._calculate_current_stats(current_data)
        
        drift_results = {}
        
        # Check user interaction distribution
        user_drift = self._check_distribution_drift(
            self.baseline_stats['avg_user_interactions'],
            self.baseline_stats['std_user_interactions'],
            current_stats['avg_user_interactions'],
            current_stats['std_user_interactions']
        )
        
        drift_results['user_interaction_drift'] = user_drift
        
        # Check item popularity distribution
        item_drift = self._check_popularity_drift(
            self.baseline_stats['item_popularity_distribution'],
            current_stats['item_popularity_distribution']
        )
        
        drift_results['item_popularity_drift'] = item_drift
        
        return drift_results
    
    def _calculate_current_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate current data statistics"""
        interactions = data.get('interactions', {})
        
        user_interaction_counts = [len(items) for items in interactions.values()]
        item_interaction_counts = {}
        
        for items in interactions.values():
            for item_id in items.keys():
                item_interaction_counts[item_id] = item_interaction_counts.get(item_id, 0) + 1
        
        return {
            'avg_user_interactions': np.mean(user_interaction_counts),
            'std_user_interactions': np.std(user_interaction_counts),
            'total_users': len(interactions),
            'total_items': len(item_interaction_counts),
            'item_popularity_distribution': list(item_interaction_counts.values())
        }
    
    def _check_distribution_drift(self, baseline_mean: float, baseline_std: float,
                                current_mean: float, current_std: float) -> Dict[str, Any]:
        """Check for distribution drift"""
        mean_drift = abs(current_mean - baseline_mean) / baseline_mean if baseline_mean > 0 else 0
        std_drift = abs(current_std - baseline_std) / baseline_std if baseline_std > 0 else 0
        
        return {
            'mean_drift': mean_drift,
            'std_drift': std_drift,
            'drift_detected': mean_drift > 0.1 or std_drift > 0.1
        }
    
    def _check_popularity_drift(self, baseline_dist: List[int], current_dist: List[int]) -> Dict[str, Any]:
        """Check for popularity distribution drift"""
        if not baseline_dist or not current_dist:
            return {'drift_detected': False}
        
        # Calculate KL divergence (simplified)
        baseline_norm = np.array(baseline_dist) / sum(baseline_dist)
        current_norm = np.array(current_dist) / sum(current_dist)
        
        # Pad arrays to same length
        max_len = max(len(baseline_norm), len(current_norm))
        baseline_padded = np.pad(baseline_norm, (0, max_len - len(baseline_norm)))
        current_padded = np.pad(current_norm, (0, max_len - len(current_norm)))
        
        # Calculate drift
        drift = np.sum(np.abs(baseline_padded - current_padded))
        
        return {
            'drift_score': drift,
            'drift_detected': drift > 0.2
        }
