"""

Hybrid Recommender combining multiple algorithms

"""

import numpy as np
from typing import List, Dict, Any, Tuple
import logging
from .base_recommender import BaseRecommender

logger = logging.getLogger(__name__)

class HybridRecommender(BaseRecommender):
    """Hybrid recommendation system combining multiple algorithms"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("HybridRecommender", config)
        
        self.models = {}
        self.weights = self.config.get('model_weights', {})
        self.ensemble_method = self.config.get('ensemble_method', 'weighted')
        
    def train(self, data: Dict[str, Any]) -> None:
        """Train all component models"""
        logger.info("Training Hybrid Recommender...")
        
        # Train Neural Collaborative Filtering
        if 'neural_collaborative' in self.weights:
            try:
                from .neural_collaborative import NeuralCollaborativeFiltering
                ncf = NeuralCollaborativeFiltering()
                ncf.train(data)
                self.models['neural_collaborative'] = ncf
                logger.info("✅ Neural Collaborative Filtering trained")
            except Exception as e:
                logger.warning(f"⚠️ NCF training failed: {e}")
        
        # Train Content-Based Recommender
        if 'content_based' in self.weights:
            try:
                from .content_based import ContentBasedRecommender
                cb = ContentBasedRecommender()
                cb.train(data)
                self.models['content_based'] = cb
                logger.info("✅ Content-Based Recommender trained")
            except Exception as e:
                logger.warning(f"⚠️ Content-Based training failed: {e}")
        
        # Train Collaborative Filtering
        if 'collaborative_filtering' in self.weights:
            try:
                from .collaborative_filtering import CollaborativeFilteringRecommender
                cf = CollaborativeFilteringRecommender()
                cf.train(data)
                self.models['collaborative_filtering'] = cf
                logger.info("✅ Collaborative Filtering trained")
            except Exception as e:
                logger.warning(f"⚠️ Collaborative Filtering training failed: {e}")
        
        self.is_trained = True
        logger.info("Hybrid Recommender training completed")
    
    def predict(self, user_id: int, history: List[int], n_recommendations: int = 10) -> List[Tuple[int, float]]:
        """Generate hybrid recommendations"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        all_recommendations = {}
        
        # Get recommendations from each model
        for model_name, model in self.models.items():
            try:
                if model_name in self.weights:
                    weight = self.weights[model_name]
                    recommendations = model.predict(user_id, history, n_recommendations * 2)
                    
                    # Weight the scores
                    for item_id, score in recommendations:
                        if item_id not in all_recommendations:
                            all_recommendations[item_id] = 0
                        all_recommendations[item_id] += score * weight
                        
            except Exception as e:
                logger.warning(f"⚠️ {model_name} prediction failed: {e}")
        
        # Convert to list and sort
        recommendations = [(item_id, score) for item_id, score in all_recommendations.items()]
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n_recommendations]
    
    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate hybrid model performance"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Evaluate each component model
        results = {}
        for model_name, model in self.models.items():
            try:
                metrics = model.evaluate(test_data)
                results[model_name] = metrics
            except Exception as e:
                logger.warning(f"⚠️ {model_name} evaluation failed: {e}")
                results[model_name] = {}
        
        # Calculate weighted average of metrics
        hybrid_metrics = {}
        if results:
            for metric in ['precision@10', 'recall@10', 'ndcg@10']:
                weighted_sum = 0
                total_weight = 0
                
                for model_name, model_metrics in results.items():
                    if metric in model_metrics and model_name in self.weights:
                        weight = self.weights[model_name]
                        weighted_sum += model_metrics[metric] * weight
                        total_weight += weight
                
                if total_weight > 0:
                    hybrid_metrics[metric] = weighted_sum / total_weight
                else:
                    hybrid_metrics[metric] = 0.0
        
        return hybrid_metrics
