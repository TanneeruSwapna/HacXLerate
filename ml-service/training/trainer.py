"""
Model training orchestrator
"""

import os
import logging
from typing import Dict, Any, List
from ..core.base_recommender import BaseRecommender
from ..models.model_manager import ModelManager
from ..models.model_evaluator import ModelEvaluator

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Orchestrates model training"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_manager = ModelManager()
        self.evaluator = ModelEvaluator()
        self.trained_models = {}
    
    def train_models(self, data: Dict[str, Any]) -> Dict[str, BaseRecommender]:
        """Train all configured models"""
        logger.info("Starting model training...")
        
        models = {}
        
        # Train Neural Collaborative Filtering
        if self.config.get('neural_collaborative', {}).get('enabled', False):
            try:
                from ..core.neural_collaborative import NeuralCollaborativeFiltering
                model = NeuralCollaborativeFiltering(self.config['neural_collaborative'])
                model.train(data)
                models['neural_collaborative'] = model
                logger.info("✅ Neural Collaborative Filtering trained")
            except Exception as e:
                logger.error(f"❌ NCF training failed: {e}")
        
        # Train Content-Based Recommender
        if self.config.get('content_based', {}).get('enabled', False):
            try:
                from ..core.content_based import ContentBasedRecommender
                model = ContentBasedRecommender(self.config['content_based'])
                model.train(data)
                models['content_based'] = model
                logger.info("✅ Content-Based Recommender trained")
            except Exception as e:
                logger.error(f"❌ Content-Based training failed: {e}")
        
        # Train Collaborative Filtering
        if self.config.get('collaborative_filtering', {}).get('enabled', False):
            try:
                from ..core.collaborative_filtering import CollaborativeFilteringRecommender
                model = CollaborativeFilteringRecommender(self.config['collaborative_filtering'])
                model.train(data)
                models['collaborative_filtering'] = model
                logger.info("✅ Collaborative Filtering trained")
            except Exception as e:
                logger.error(f"❌ Collaborative Filtering training failed: {e}")
        
        # Train Hybrid Recommender
        if self.config.get('hybrid', {}).get('enabled', False):
            try:
                from ..core.hybrid_recommender import HybridRecommender
                model = HybridRecommender(self.config['hybrid'])
                model.train(data)
                models['hybrid'] = model
                logger.info("✅ Hybrid Recommender trained")
            except Exception as e:
                logger.error(f"❌ Hybrid training failed: {e}")
        
        self.trained_models = models
        logger.info(f"Training completed: {len(models)} models trained")
        return models
    
    def save_models(self, models: Dict[str, BaseRecommender]):
        """Save trained models"""
        if not self.config.get('training', {}).get('save_models', False):
            return
        
        model_dir = self.config.get('training', {}).get('model_dir', 'models/checkpoints')
        os.makedirs(model_dir, exist_ok=True)
        
        for model_name, model in models.items():
            try:
                model_path = os.path.join(model_dir, f"{model_name}_model.pkl")
                model.save_model(model_path)
                logger.info(f"✅ {model_name} model saved")
            except Exception as e:
                logger.error(f"❌ Failed to save {model_name} model: {e}")
    
    def evaluate_models(self, models: Dict[str, BaseRecommender], test_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Evaluate trained models"""
        if not self.config.get('training', {}).get('evaluate_models', False):
            return {}
        
        logger.info("Evaluating models...")
        results = {}
        
        for model_name, model in models.items():
            try:
                metrics = model.evaluate(test_data)
                results[model_name] = metrics
                logger.info(f"✅ {model_name} evaluation completed")
            except Exception as e:
                logger.error(f"❌ {model_name} evaluation failed: {e}")
                results[model_name] = {}
        
        return results
