"""
Feature engineering utilities
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """Engineers features for ML models"""
    
    def __init__(self):
        self.feature_stats = {}
    
    def create_user_features(self, interactions: Dict[int, Dict[int, float]], 
                           user_features: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, float]]:
        """Create enhanced user features"""
        logger.info("Creating user features...")
        
        enhanced_user_features = {}
        
        for user_id, items in interactions.items():
            features = {}
            
            # Basic interaction features
            features['total_interactions'] = len(items)
            features['avg_rating'] = np.mean(list(items.values()))
            features['rating_std'] = np.std(list(items.values()))
            
            # Interaction diversity
            features['unique_categories'] = len(set([
                item_features.get('category', 'unknown') 
                for item_id, item_features in items.items()
            ]))
            
            # Business features (if available)
            if user_id in user_features:
                business_info = user_features[user_id]
                features['annual_revenue'] = business_info.get('annual_revenue', 0)
                features['employee_count'] = business_info.get('employee_count', 0)
                features['credit_limit'] = business_info.get('credit_limit', 0)
            
            enhanced_user_features[user_id] = features
        
        logger.info(f"Created features for {len(enhanced_user_features)} users")
        return enhanced_user_features
    
    def create_item_features(self, item_features: Dict[int, Dict[str, Any]], 
                           interactions: Dict[int, Dict[int, float]]) -> Dict[int, Dict[str, float]]:
        """Create enhanced item features"""
        logger.info("Creating item features...")
        
        # Calculate item popularity
        item_popularity = {}
        for user_items in interactions.values():
            for item_id in user_items.keys():
                item_popularity[item_id] = item_popularity.get(item_id, 0) + 1
        
        enhanced_item_features = {}
        
        for item_id, features in item_features.items():
            enhanced_features = {}
            
            # Original features
            enhanced_features.update(features)
            
            # Popularity features
            enhanced_features['popularity'] = item_popularity.get(item_id, 0)
            enhanced_features['log_popularity'] = np.log1p(item_popularity.get(item_id, 0))
            
            # Price features (if available)
            if 'price' in features:
                price = float(features['price'])
                enhanced_features['log_price'] = np.log1p(price)
                enhanced_features['price_category'] = self._categorize_price(price)
            
            # Rating features (if available)
            if 'rating' in features:
                rating = float(features['rating'])
                enhanced_features['rating_category'] = self._categorize_rating(rating)
            
            enhanced_item_features[item_id] = enhanced_features
        
        logger.info(f"Created features for {len(enhanced_item_features)} items")
        return enhanced_item_features
    
    def _categorize_price(self, price: float) -> int:
        """Categorize price into buckets"""
        if price < 100:
            return 0  # Low price
        elif price < 500:
            return 1  # Medium price
        elif price < 1000:
            return 2  # High price
        else:
            return 3  # Very high price
    
    def _categorize_rating(self, rating: float) -> int:
        """Categorize rating into buckets"""
        if rating < 3.0:
            return 0  # Low rating
        elif rating < 4.0:
            return 1  # Medium rating
        else:
            return 2  # High rating
    
    def create_interaction_features(self, interactions: Dict[int, Dict[int, float]]) -> Dict[str, float]:
        """Create global interaction features"""
        logger.info("Creating interaction features...")
        
        all_ratings = []
        user_interaction_counts = []
        item_interaction_counts = {}
        
        for user_id, items in interactions.items():
            user_interaction_counts.append(len(items))
            all_ratings.extend(items.values())
            
            for item_id in items.keys():
                item_interaction_counts[item_id] = item_interaction_counts.get(item_id, 0) + 1
        
        features = {
            'total_users': len(interactions),
            'total_items': len(set(item for items in interactions.values() for item in items.keys())),
            'total_interactions': sum(user_interaction_counts),
            'avg_interactions_per_user': np.mean(user_interaction_counts),
            'std_interactions_per_user': np.std(user_interaction_counts),
            'avg_rating': np.mean(all_ratings) if all_ratings else 0,
            'std_rating': np.std(all_ratings) if all_ratings else 0,
            'sparsity': 1 - (sum(user_interaction_counts) / (len(interactions) * len(set(item for items in interactions.values() for item in items.keys()))))
        }
        
        logger.info("Interaction features created")
        return features
