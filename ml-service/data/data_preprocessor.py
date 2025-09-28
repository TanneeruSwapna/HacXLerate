"""
Data preprocessing utilities
"""

import pandas as pd  # pyright: ignore[reportMissingImports]
import numpy as np  # pyright: ignore[reportMissingImports]
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Preprocesses data for ML models"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
    
    def clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and preprocess data"""
        logger.info("Cleaning data...")
        
        # Clean interactions
        interactions = data.get('interactions', {})
        cleaned_interactions = {}
        
        for user_id, items in interactions.items():
            if items:  # Only keep users with interactions
                cleaned_items = {}
                for item_id, rating in items.items():
                    if rating > 0:  # Only keep positive interactions
                        cleaned_items[item_id] = rating
                
                if cleaned_items:  # Only keep users with valid interactions
                    cleaned_interactions[user_id] = cleaned_items
        
        data['interactions'] = cleaned_interactions
        
        # Clean item features
        item_features = data.get('item_features', {})
        cleaned_item_features = {}
        
        for item_id, features in item_features.items():
            cleaned_features = {}
            for feature_name, value in features.items():
                if value is not None and str(value).strip():  # Remove None and empty values
                    cleaned_features[feature_name] = value
            
            if cleaned_features:  # Only keep items with valid features
                cleaned_item_features[item_id] = cleaned_features
        
        data['item_features'] = cleaned_item_features
        
        logger.info(f"Data cleaned: {len(cleaned_interactions)} users, {len(cleaned_item_features)} items")
        return data
    
    def normalize_ratings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize ratings to 0-1 range"""
        logger.info("Normalizing ratings...")
        
        interactions = data['interactions']
        all_ratings = []
        
        # Collect all ratings
        for user_items in interactions.values():
            all_ratings.extend(user_items.values())
        
        if all_ratings:
            min_rating = min(all_ratings)
            max_rating = max(all_ratings)
            
            # Normalize ratings
            for user_id, items in interactions.items():
                for item_id, rating in items.items():
                    normalized_rating = (rating - min_rating) / (max_rating - min_rating)
                    interactions[user_id][item_id] = normalized_rating
        
        logger.info("Ratings normalized")
        return data
    
    def filter_sparse_users_items(self, data: Dict[str, Any], 
                                 min_user_interactions: int = 5,
                                 min_item_interactions: int = 3) -> Dict[str, Any]:
        """Filter out sparse users and items"""
        logger.info("Filtering sparse users and items...")
        
        interactions = data['interactions']
        item_features = data['item_features']
        
        # Count interactions per user and item
        user_counts = {}
        item_counts = {}
        
        for user_id, items in interactions.items():
            user_counts[user_id] = len(items)
            for item_id in items.keys():
                item_counts[item_id] = item_counts.get(item_id, 0) + 1
        
        # Filter users
        filtered_interactions = {}
        for user_id, items in interactions.items():
            if user_counts[user_id] >= min_user_interactions:
                filtered_items = {}
                for item_id, rating in items.items():
                    if item_counts.get(item_id, 0) >= min_item_interactions:
                        filtered_items[item_id] = rating
                
                if filtered_items:
                    filtered_interactions[user_id] = filtered_items
        
        # Filter item features
        filtered_item_features = {}
        for item_id, features in item_features.items():
            if item_counts.get(item_id, 0) >= min_item_interactions:
                filtered_item_features[item_id] = features
        
        data['interactions'] = filtered_interactions
        data['item_features'] = filtered_item_features
        
        logger.info(f"Filtered: {len(filtered_interactions)} users, {len(filtered_item_features)} items")
        return data
    
    def split_data(self, data: Dict[str, Any], test_ratio: float = 0.2) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Split data into train and test sets"""
        logger.info(f"Splitting data with test ratio: {test_ratio}")
        
        interactions = data['interactions']
        train_interactions = {}
        test_interactions = {}
        
        for user_id, items in interactions.items():
            if len(items) > 1:  # Only split users with multiple interactions
                item_list = list(items.items())
                test_size = max(1, int(len(item_list) * test_ratio))
                
                # Randomly select test items
                np.random.seed(42)
                test_indices = np.random.choice(len(item_list), test_size, replace=False)
                
                train_items = {}
                test_items = {}
                
                for i, (item_id, rating) in enumerate(item_list):
                    if i in test_indices:
                        test_items[item_id] = rating
                    else:
                        train_items[item_id] = rating
                
                if train_items:
                    train_interactions[user_id] = train_items
                if test_items:
                    test_interactions[user_id] = test_items
            else:
                # Users with single interaction go to train set
                train_interactions[user_id] = items
        
        train_data = {
            'interactions': train_interactions,
            'item_features': data['item_features'],
            'user_features': data['user_features']
        }
        
        test_data = {
            'interactions': test_interactions,
            'item_features': data['item_features'],
            'user_features': data['user_features']
        }
        
        logger.info(f"Data split: {len(train_interactions)} train users, {len(test_interactions)} test users")
        return train_data, test_data
