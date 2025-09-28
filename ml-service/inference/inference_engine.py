"""
Real-time inference engine
"""

import time
from typing import Dict, Any, List, Tuple
import logging

logger = logging.getLogger(__name__)

class InferenceEngine:
    """Real-time inference engine for recommendations"""
    
    def __init__(self, models: Dict[str, Any]):
        self.models = models
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    def get_recommendations(self, user_id: int, history: List[int], 
                          n_recommendations: int = 10, 
                          model_name: str = 'hybrid') -> List[Tuple[int, float]]:
        """Get real-time recommendations"""
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{user_id}_{hash(tuple(sorted(history)))}_{n_recommendations}"
        if cache_key in self.cache:
            cached_result, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                logger.info(f"Cache hit for user {user_id}")
                return cached_result
        
        # Get recommendations from model
        if model_name not in self.models:
            logger.error(f"Model {model_name} not found")
            return []
        
        try:
            model = self.models[model_name]
            recommendations = model.predict(user_id, history, n_recommendations)
            
            # Cache the result
            self.cache[cache_key] = (recommendations, time.time())
            
            # Log performance
            inference_time = time.time() - start_time
            logger.info(f"Recommendations generated in {inference_time:.3f}s")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return []
    
    def get_batch_recommendations(self, requests: List[Dict[str, Any]]) -> List[List[Tuple[int, float]]]:
        """Get batch recommendations"""
        results = []
        
        for request in requests:
            user_id = request.get('user_id')
            history = request.get('history', [])
            n_recommendations = request.get('n_recommendations', 10)
            model_name = request.get('model_name', 'hybrid')
            
            recommendations = self.get_recommendations(
                user_id, history, n_recommendations, model_name
            )
            results.append(recommendations)
        
        return results
    
    def clear_cache(self):
        """Clear recommendation cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.cache),
            'cache_ttl': self.cache_ttl
        }
