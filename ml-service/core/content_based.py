"""
Content-Based Filtering for B2B recommendations
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import List, Dict, Any, Tuple
import logging
from .base_recommender import BaseRecommender

logger = logging.getLogger(__name__)

class ContentBasedRecommender(BaseRecommender):
    """Content-based recommendation system"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ContentBasedRecommender", config)
        
        self.similarity_threshold = self.config.get('similarity_threshold', 0.7)
        self.feature_weights = self.config.get('feature_weights', {
            'category': 0.4,
            'brand': 0.3,
            'price': 0.2,
            'rating': 0.1
        })
        self.similarity_metric = self.config.get('similarity_metric', 'cosine')
        
        self.item_features = None
        self.feature_matrix = None
        self.item_ids = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
    
    def train(self, data: Dict[str, Any]) -> None:
        """Train the content-based model"""
        logger.info("Training Content-Based Recommender...")
        
        item_features = data['item_features']
        self.item_features = item_features
        
        # Create feature matrix
        self._create_feature_matrix(item_features)
        
        self.is_trained = True
        logger.info("Content-Based Recommender training completed")
    
    def _create_feature_matrix(self, item_features: Dict[int, Dict[str, Any]]):
        """Create feature matrix from item features"""
        feature_vectors = []
        self.item_ids = []
        
        for item_id, features in item_features.items():
            feature_vector = []
            
            # Extract and encode features
            for feature_name, weight in self.feature_weights.items():
                if feature_name in features:
                    value = features[feature_name]
                    
                    if feature_name in ['price', 'rating']:
                        # Numerical features
                        feature_vector.append(float(value))
                    else:
                        # Categorical features - use hash encoding
                        encoded_value = hash(str(value)) % 1000
                        feature_vector.append(encoded_value)
                else:
                    feature_vector.append(0)
            
            feature_vectors.append(feature_vector)
            self.item_ids.append(item_id)
        
        # Normalize features
        self.feature_matrix = self.scaler.fit_transform(feature_vectors)
        
        logger.info(f"Feature matrix created: {self.feature_matrix.shape}")
    
    def predict(self, user_id: int, history: List[int], n_recommendations: int = 10) -> List[Tuple[int, float]]:
        """Generate content-based recommendations"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Get user's preferred features
        user_preferences = self._get_user_preferences(history)
        
        # Calculate similarities
        similarities = self._calculate_similarities(user_preferences)
        
        # Filter out items in history
        recommendations = []
        for i, (item_id, similarity) in enumerate(zip(self.item_ids, similarities)):
            if item_id not in history and similarity > self.similarity_threshold:
                recommendations.append((item_id, similarity))
        
        # Sort by similarity and return top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]
    
    def _get_user_preferences(self, history: List[int]) -> np.ndarray:
        """Get user's feature preferences from history"""
        if not history:
            return np.zeros(self.feature_matrix.shape[1])
        
        # Get features of items in user's history
        history_features = []
        for item_id in history:
            if item_id in self.item_ids:
                idx = self.item_ids.index(item_id)
                history_features.append(self.feature_matrix[idx])
        
        if not history_features:
            return np.zeros(self.feature_matrix.shape[1])
        
        # Average the features
        user_preferences = np.mean(history_features, axis=0)
        return user_preferences.reshape(1, -1)
    
    def _calculate_similarities(self, user_preferences: np.ndarray) -> np.ndarray:
        """Calculate similarities between user preferences and items"""
        if self.similarity_metric == 'cosine':
            similarities = cosine_similarity(user_preferences, self.feature_matrix)[0]
        else:
            # Default to cosine similarity
            similarities = cosine_similarity(user_preferences, self.feature_matrix)[0]
        
        return similarities
    
    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate content-based model performance"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Simple evaluation metrics
        test_interactions = test_data['interactions']
        
        precision_scores = []
        recall_scores = []
        
        for user_id, items in test_interactions.items():
            if len(items) > 1:  # User with multiple interactions
                # Split into history and test items
                item_list = list(items.keys())
                history = item_list[:-1]  # All but last item
                test_item = item_list[-1]  # Last item
                
                # Get recommendations
                recommendations = self.predict(user_id, history, n_recommendations=10)
                recommended_items = [item_id for item_id, _ in recommendations]
                
                # Calculate precision and recall
                if test_item in recommended_items:
                    precision_scores.append(1.0 / len(recommended_items))
                    recall_scores.append(1.0)
                else:
                    precision_scores.append(0.0)
                    recall_scores.append(0.0)
        
        return {
            'precision@10': np.mean(precision_scores) if precision_scores else 0.0,
            'recall@10': np.mean(recall_scores) if recall_scores else 0.0,
            'coverage': len(set([item_id for _, items in test_interactions.items() for item_id in items.keys()])) / len(self.item_ids)
        }
