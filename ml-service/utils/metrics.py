"""
Evaluation metrics utilities
"""

import numpy as np
from typing import List, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Metrics:
    """Evaluation metrics for recommendation systems"""
    
    @staticmethod
    def precision_at_k(recommendations: List[Tuple[int, float]], 
                      relevant_items: List[int], k: int = 10) -> float:
        """Calculate Precision@K"""
        if not recommendations or k == 0:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        relevant_in_top_k = len(set(top_k_items) & set(relevant_items))
        return relevant_in_top_k / k
    
    @staticmethod
    def recall_at_k(recommendations: List[Tuple[int, float]], 
                   relevant_items: List[int], k: int = 10) -> float:
        """Calculate Recall@K"""
        if not relevant_items:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        relevant_in_top_k = len(set(top_k_items) & set(relevant_items))
        return relevant_in_top_k / len(relevant_items)
    
    @staticmethod
    def ndcg_at_k(recommendations: List[Tuple[int, float]], 
                 relevant_items: List[int], k: int = 10) -> float:
        """Calculate NDCG@K"""
        if not recommendations or k == 0:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        
        # Calculate DCG
        dcg = 0.0
        for i, item_id in enumerate(top_k_items):
            if item_id in relevant_items:
                dcg += 1.0 / np.log2(i + 2)
        
        # Calculate IDCG
        idcg = 0.0
        for i in range(min(len(relevant_items), k)):
            idcg += 1.0 / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0.0
    
    @staticmethod
    def map_at_k(recommendations: List[Tuple[int, float]], 
                relevant_items: List[int], k: int = 10) -> float:
        """Calculate MAP@K"""
        if not recommendations or k == 0:
            return 0.0
        
        top_k_items = [item_id for item_id, _ in recommendations[:k]]
        
        precision_sum = 0.0
        relevant_count = 0
        
        for i, item_id in enumerate(top_k_items):
            if item_id in relevant_items:
                relevant_count += 1
                precision_sum += relevant_count / (i + 1)
        
        return precision_sum / len(relevant_items) if relevant_items else 0.0
    
    @staticmethod
    def coverage(recommendations: List[Tuple[int, float]], 
                total_items: int) -> float:
        """Calculate Coverage"""
        if total_items == 0:
            return 0.0
        
        recommended_items = set(item_id for item_id, _ in recommendations)
        return len(recommended_items) / total_items
    
    @staticmethod
    def diversity(recommendations: List[Tuple[int, float]], 
                 item_features: Dict[int, Dict[str, Any]]) -> float:
        """Calculate Diversity (category diversity)"""
        if not recommendations:
            return 0.0
        
        categories = []
        for item_id, _ in recommendations:
            if item_id in item_features:
                category = item_features[item_id].get('category', 'unknown')
                categories.append(category)
        
        unique_categories = len(set(categories))
        total_categories = len(categories)
        
        return unique_categories / total_categories if total_categories > 0 else 0.0
    
    @staticmethod
    def novelty(recommendations: List[Tuple[int, float]], 
               item_popularity: Dict[int, int]) -> float:
        """Calculate Novelty (inverse popularity)"""
        if not recommendations:
            return 0.0
        
        avg_popularity = 0.0
        count = 0
        
        for item_id, _ in recommendations:
            if item_id in item_popularity:
                avg_popularity += item_popularity[item_id]
                count += 1
        
        if count == 0:
            return 0.0
        
        avg_popularity /= count
        max_popularity = max(item_popularity.values()) if item_popularity else 1
        
        # Convert to novelty (lower popularity = higher novelty)
        return 1 - (avg_popularity / max_popularity)
