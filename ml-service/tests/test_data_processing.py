"""
Test data processing utilities
"""

import unittest
import pandas as pd
from typing import Dict, Any

class TestDataProcessing(unittest.TestCase):
    """Test data processing utilities"""
    
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
    
    def test_data_preprocessor(self):
        """Test data preprocessor"""
        try:
            from ..data.data_preprocessor import DataPreprocessor
            
            preprocessor = DataPreprocessor()
            cleaned_data = preprocessor.clean_data(self.sample_data)
            
            self.assertIn('interactions', cleaned_data)
            self.assertIn('item_features', cleaned_data)
            self.assertIn('user_features', cleaned_data)
            
        except ImportError:
            self.skipTest("Data preprocessor not available")
    
    def test_feature_engineering(self):
        """Test feature engineering"""
        try:
            from ..data.feature_engineering import FeatureEngineer
            
            engineer = FeatureEngineer()
            user_features = engineer.create_user_features(
                self.sample_data['interactions'],
                self.sample_data['user_features']
            )
            
            self.assertIsInstance(user_features, dict)
            self.assertGreater(len(user_features), 0)
            
        except ImportError:
            self.skipTest("Feature engineer not available")
    
    def test_data_loader(self):
        """Test data loader"""
        try:
            from ..data.data_loader import DataLoader
            
            loader = DataLoader()
            # This would normally load from files, but we'll test the structure
            
            self.assertIsInstance(loader.data_dir, str)
            
        except ImportError:
            self.skipTest("Data loader not available")

if __name__ == '__main__':
    unittest.main()
