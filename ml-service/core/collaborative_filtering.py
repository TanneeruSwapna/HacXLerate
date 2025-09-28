"""
Collaborative Filtering for B2B recommendations
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from typing import List, Dict, Any, Tuple
import logging
from .base_recommender import BaseRecommender

logger = logging.getLogger(__name__)

class CollaborativeFilteringRecommender(BaseRecommender):
    """Collaborative filtering recommendation system"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("CollaborativeFilteringRecommender", config)
        
        self.similarity_metric = self.config.get('similarity_metric', 'cosine')
        self.min_similarity = self.config.get('min_similarity', 0.1)
        self.max_neighbors = self.config.get('max_neighbors', 50)
        self.min_common_items = self.config.get('min_common_items', 5)
        
        self.user_item_matrix = None
        self.user_similarity_matrix = None
        self.user_ids = None
        self.item_ids = None
    
    def train(self, data: Dict[str, Any]) -> None:
        """Train the collaborative filtering model"""
        logger.info("Training Collaborative Filtering Recommender...")
        
        interactions = data['interactions']
        
        # Create user-item matrix
        self._create_user_item_matrix(interactions)
        
        # Calculate user similarities
        self._calculate_user_similarities()
        
        self.is_trained = True
        logger.info("Collaborative Filtering Recommender training completed")
    
    def _create_user_item_matrix(self, interactions: Dict[int, Dict[int, float]]):
        """Create user-item interaction matrix"""
        # Get all users and items
        all_users = list(interactions.keys())
        all_items = set()
        
        for user_items in interactions.values():
            all_items.update(user_items.keys())
        
        all_items = list(all_items)
        
        # Create mappings
        self.user_ids = all_users
        self.item_ids = all_items
        user_to_idx = {user_id: idx for idx, user_id in enumerate(all_users)}
        item_to_idx = {item_id: idx for idx, item_id in enumerate(all_items)}
        
        # Create matrix
        n_users = len(all_users)
        n_items = len(all_items)
        self.user_item_matrix = np.zeros((n_users, n_items))
        
        # Fill matrix with interactions
        for user_id, items in interactions.items():
            user_idx = user_to_idx[user_id]
            for item_id, rating in items.items():
                item_idx = item_to_idx[item_id]
                self.user_item_matrix[user_idx, item_idx] = rating
        
        logger.info(f"User-item matrix created: {self.user_item_matrix.shape}")
    
    def _calculate_user_similarities(self):
        """Calculate user similarity matrix"""
        if self.similarity_metric == 'cosine':
            self.user_similarity_matrix = cosine_similarity(self.user_item_matrix)
        elif self.similarity_metric == 'pearson':
            # Pearson correlation
            self.user_similarity_matrix = np.corrcoef(self.user_item_matrix)
            # Replace NaN with 0
            self.user_similarity_matrix = np.nan_to_num(self.user_similarity_matrix)
        else:
            # Default to cosine
            self.user_similarity_matrix = cosine_similarity(self.user_item_matrix)
        
        # Set diagonal to 0 (self-similarity)
        np.fill_diagonal(self.user_similarity_matrix, 0)
        
        logger.info(f"User similarity matrix created: {self.user_similarity_matrix.shape}")
    
    def predict(self, user_id: int, history: List[int], n_recommendations: int = 10) -> List[Tuple[int, float]]:
        """Generate collaborative filtering recommendations"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        if user_id not in self.user_ids:
            return []
        
        user_idx = self.user_ids.index(user_id)
        
        # Get similar users
        user_similarities = self.user_similarity_matrix[user_idx]
        similar_users = np.argsort(user_similarities)[::-1]  # Sort by similarity
        
        # Filter similar users
        valid_similar_users = []
        for sim_user_idx in similar_users:
            if (user_similarities[sim_user_idx] > self.min_similarity and 
                len(valid_similar_users) < self.max_neighbors):
                valid_similar_users.append(sim_user_idx)
        
        # Calculate item scores
        item_scores = {}
        user_items = set(history)
        
        for sim_user_idx in valid_similar_users:
            similarity = user_similarities[sim_user_idx]
            sim_user_items = self.user_item_matrix[sim_user_idx]
            
            # Find items liked by similar user but not by target user
            for item_idx, rating in enumerate(sim_user_items):
                if rating > 0 and self.item_ids[item_idx] not in user_items:
                    item_id = self.item_ids[item_idx]
                    if item_id not in item_scores:
                        item_scores[item_id] = 0
                    item_scores[item_id] += similarity * rating
        
        # Convert to list and sort
        recommendations = [(item_id, score) for item_id, score in item_scores.items()]
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n_recommendations]
    
    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate collaborative filtering model performance"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        test_interactions = test_data['interactions']
        
        precision_scores = []
        recall_scores = []
        ndcg_scores = []
        
        for user_id, items in test_interactions.items():
            if user_id in self.user_ids and len(items) > 1:
                # Split into history and test items
                item_list = list(items.keys())
                history = item_list[:-1]
                test_item = item_list[-1]
                
                # Get recommendations
                recommendations = self.predict(user_id, history, n_recommendations=10)
                recommended_items = [item_id for item_id, _ in recommendations]
                
                # Calculate metrics
                if test_item in recommended_items:
                    rank = recommended_items.index(test_item) + 1
                    precision_scores.append(1.0 / rank)
                    recall_scores.append(1.0)
                    ndcg_scores.append(1.0 / np.log2(rank + 1))
                else:
                    precision_scores.append(0.0)
                    recall_scores.append(0.0)
                    ndcg_scores.append(0.0)
        
        return {
            'precision@10': np.mean(precision_scores) if precision_scores else 0.0,
            'recall@10': np.mean(recall_scores) if recall_scores else 0.0,
            'ndcg@10': np.mean(ndcg_scores) if ndcg_scores else 0.0,
            'coverage': len(set([item_id for _, items in test_interactions.items() for item_id in items.keys()])) / len(self.item_ids)
        }
