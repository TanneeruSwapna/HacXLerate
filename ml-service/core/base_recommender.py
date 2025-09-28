"""
Base recommendation class for all ML algorithms
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class BaseRecommender(ABC):
    """Base class for all recommendation algorithms"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the recommender
        
        Args:
            name: Name of the recommender
            config: Configuration parameters
        """
        self.name = name
        self.config = config or {}
        self.is_trained = False
        self.model = None
        
    @abstractmethod
    def train(self, data: Dict[str, Any]) -> None:
        """
        Train the recommendation model
        
        Args:
            data: Training data dictionary
        """
        pass
    
    @abstractmethod
    def predict(self, user_id: int, history: List[int], n_recommendations: int = 10) -> List[Tuple[int, float]]:
        """
        Generate recommendations for a user
        
        Args:
            user_id: User ID
            history: User's purchase/view history
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (item_id, score) tuples
        """
        pass
    
    @abstractmethod
    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate model performance
        
        Args:
            test_data: Test data dictionary
            
        Returns:
            Dictionary of evaluation metrics
        """
        pass
    
    def save_model(self, filepath: str) -> None:
        """Save the trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        # Implementation depends on the specific model type
        logger.info(f"Saving {self.name} model to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """Load a trained model"""
        # Implementation depends on the specific model type
        logger.info(f"Loading {self.name} model from {filepath}")
        self.is_trained = True
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'name': self.name,
            'is_trained': self.is_trained,
            'config': self.config
        }
