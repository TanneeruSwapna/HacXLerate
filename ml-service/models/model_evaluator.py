"""
Model evaluation utilities
"""

import numpy as np
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Evaluates model performance"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_precision_at_k(self, recommendations: List[Tuple[int, float]], 
                                relevant_items: List[int], k: int = 10) -> float:
        """Calculate Precision@K"""
        if not recommendations or k == 0:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        relevant_in_top_k = len(set(top_k_items) & set(relevant_items))
        return relevant_in_top_k / k
    
    def calculate_recall_at_k(self, recommendations: List[Tuple[int, float]], 
                             relevant_items: List[int], k: int = 10) -> float:
        """Calculate Recall@K"""
        if not relevant_items:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        relevant_in_top_k = len(set(top_k_items) & set(relevant_items))
        return relevant_in_top_k / len(relevant_items)
    
    def calculate_ndcg_at_k(self, recommendations: List[Tuple[int, float]], 
                           relevant_items: List[int], k: int = 10) -> float:
        """Calculate NDCG@K"""
        if not recommendations or k == 0:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        
        # Calculate DCG
        dcg = 0.0
        for i, item_id in enumerate(top_k_items):
            if item_id in relevant_items:
                dcg += 1.0 / np.log2(i + 2)  # +2 because log2(1) = 0
        
        # Calculate IDCG (ideal DCG)
        idcg = 0.0
        for i in range(min(len(relevant_items), k)):
            idcg += 1.0 / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0.0
    
    def evaluate_model(self, model, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate model performance"""
        metrics = {
            'precision@10': 0.0,
            'recall@10': 0.0,
            'ndcg@10': 0.0,
            'coverage': 0.0
        }
        
        try:
            interactions = test_data['interactions']
            total_precision = 0.0
            total_recall = 0.0
            total_ndcg = 0.0
            count = 0
            
            for user_id, items in interactions.items():
                if len(items) > 1:
                    # Split into history and test items
                    item_list = list(items.keys())
                    history = item_list[:-1]
                    test_item = item_list[-1]
                    
                    # Get recommendations
                    recommendations = model.predict(user_id, history, n_recommendations=10)
                    
                    # Calculate metrics
                    precision = self.calculate_precision_at_k(recommendations, [test_item])
                    recall = self.calculate_recall_at_k(recommendations, [test_item])
                    ndcg = self.calculate_ndcg_at_k(recommendations, [test_item])
                    
                    total_precision += precision
                    total_recall += recall
                    total_ndcg += ndcg
                    count += 1
            
            if count > 0:
                metrics['precision@10'] = total_precision / count
                metrics['recall@10'] = total_recall / count
                metrics['ndcg@10'] = total_ndcg / count
            
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
        
        return metrics
