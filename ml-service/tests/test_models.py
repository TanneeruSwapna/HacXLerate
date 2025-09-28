"""
Test ML models
"""

import unittest
import numpy as np
from typing import Dict, Any

class TestModels(unittest.TestCase):
    """Test ML models"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = {
            'interactions': {
                1: {101: 5, 102: 4, 103: 3},
                2: {101: 4, 102: 5, 104: 4},
                3: {102: 3, 103: 4, 105: 5}
            },
            'item_features': {
                101: {'category': 'A', 'brand': 'X', 'price': 100, 'rating': 4.5},
                102: {'category': 'B', 'brand': 'Y', 'price': 200, 'rating': 4.0},
                103: {'category': 'A', 'brand': 'Z', 'price': 150, 'rating': 3.5},
                104: {'category': 'C', 'brand': 'X', 'price': 300, 'rating': 4.8},
                105: {'category': 'B', 'brand': 'Y', 'price': 250, 'rating': 4.2}
            },
            'user_features': {
                1: {'business_type': 'Manufacturer', 'industry': 'Tech'},
                2: {'business_type': 'Retailer', 'industry': 'Retail'},
                3: {'business_type': 'Distributor', 'industry': 'Logistics'}
            }
        }
    
    def test_content_based_recommender(self):
        """Test content-based recommender"""
        try:
            from ..core.content_based import ContentBasedRecommender
            
            model = ContentBasedRecommender()
            model.train(self.sample_data)
            
            recommendations = model.predict(1, [101], n_recommendations=3)
            
            self.assertIsInstance(recommendations, list)
            self.assertLessEqual(len(recommendations), 3)
            
            for item_id, score in recommendations:
                self.assertIsInstance(item_id, int)
                self.assertIsInstance(score, (int, float))
                
        except ImportError:
            self.skipTest("Content-based recommender not available")
    
    def test_collaborative_filtering(self):
        """Test collaborative filtering"""
        try:
            from ..core.collaborative_filtering import CollaborativeFilteringRecommender
            
            model = CollaborativeFilteringRecommender()
            model.train(self.sample_data)
            
            recommendations = model.predict(1, [101], n_recommendations=3)
            
            self.assertIsInstance(recommendations, list)
            self.assertLessEqual(len(recommendations), 3)
            
        except ImportError:
            self.skipTest("Collaborative filtering not available")
    
    def test_hybrid_recommender(self):
        """Test hybrid recommender"""
        try:
            from ..core.hybrid_recommender import HybridRecommender
            
            model = HybridRecommender()
            model.train(self.sample_data)
            
            recommendations = model.predict(1, [101], n_recommendations=3)
            
            self.assertIsInstance(recommendations, list)
            self.assertLessEqual(len(recommendations), 3)
            
        except ImportError:
            self.skipTest("Hybrid recommender not available")

if __name__ == '__main__':
    unittest.main()
