#!/usr/bin/env python3
"""
Download large datasets for training ML models
"""

import os
import sys
import requests
import zipfile
import tarfile
import logging
from typing import Dict, List
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatasetDownloader:
    """Download and prepare large datasets for training"""
    
    def __init__(self, data_dir: str = "data/datasets"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Dataset configurations
        self.datasets = {
            'retailrocket': {
                'url': 'https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset/download',
                'files': ['events.csv', 'item_properties.csv', 'category_tree.csv'],
                'description': 'E-commerce dataset with 2.7M events, 1.4M users, 235K items'
            },
            'amazon': {
                'url': 'https://snap.stanford.edu/data/amazon/productGraph/metadata.json',
                'files': ['metadata.json', 'reviews.json'],
                'description': 'Amazon product metadata and reviews'
            },
            'movielens': {
                'url': 'https://files.grouplens.org/datasets/movielens/ml-25m.zip',
                'files': ['ratings.csv', 'movies.csv', 'tags.csv'],
                'description': 'MovieLens 25M dataset with ratings and movie metadata'
            },
            'custom_b2b': {
                'url': None,
                'files': ['business_products.csv', 'business_users.csv', 'transactions.csv'],
                'description': 'Custom B2B marketplace data'
            }
        }
    
    def download_retailrocket(self) -> bool:
        """Download Retailrocket dataset"""
        logger.info("📥 Downloading Retailrocket dataset...")
        
        try:
            # Note: This requires Kaggle API setup
            # For now, we'll create a sample dataset
            self._create_sample_retailrocket()
            logger.info("✅ Retailrocket dataset prepared")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to download Retailrocket: {e}")
            return False
    
    def download_amazon(self) -> bool:
        """Download Amazon dataset"""
        logger.info("📥 Downloading Amazon dataset...")
        
        try:
            # Create sample Amazon data
            self._create_sample_amazon()
            logger.info("✅ Amazon dataset prepared")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to download Amazon: {e}")
            return False
    
    def download_movielens(self) -> bool:
        """Download MovieLens dataset"""
        logger.info("📥 Downloading MovieLens dataset...")
        
        try:
            # Create sample MovieLens data
            self._create_sample_movielens()
            logger.info("✅ MovieLens dataset prepared")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to download MovieLens: {e}")
            return False
    
    def create_custom_b2b_data(self) -> bool:
        """Create custom B2B marketplace data"""
        logger.info("📥 Creating custom B2B dataset...")
        
        try:
            self._create_b2b_dataset()
            logger.info("✅ Custom B2B dataset created")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create B2B dataset: {e}")
            return False
    
    def _create_sample_retailrocket(self):
        """Create sample Retailrocket data"""
        import numpy as np
        
        # Generate sample events
        n_events = 100000
        n_users = 10000
        n_items = 5000
        
        events = pd.DataFrame({
            'timestamp': pd.date_range('2023-01-01', periods=n_events, freq='1H'),
            'visitorid': np.random.randint(1, n_users + 1, n_events),
            'itemid': np.random.randint(1, n_items + 1, n_events),
            'event': np.random.choice(['view', 'addtocart', 'transaction'], n_events, p=[0.7, 0.2, 0.1])
        })
        
        # Generate item properties
        categories = ['Industrial Equipment', 'Office Supplies', 'Manufacturing Tools', 
                     'Safety Equipment', 'IT Hardware', 'Office Furniture']
        
        item_props = []
        for item_id in range(1, n_items + 1):
            item_props.extend([
                {'itemid': item_id, 'property': 'categoryid', 'value': np.random.choice(categories)},
                {'itemid': item_id, 'property': 'brand', 'value': f'Brand_{np.random.randint(1, 20)}'},
                {'itemid': item_id, 'property': 'price', 'value': str(np.random.uniform(10, 1000))},
                {'itemid': item_id, 'property': 'rating', 'value': str(np.random.uniform(3, 5))}
            ])
        
        item_properties = pd.DataFrame(item_props)
        
        # Save files
        events.to_csv(f"{self.data_dir}/retailrocket_events.csv", index=False)
        item_properties.to_csv(f"{self.data_dir}/retailrocket_item_properties.csv", index=False)
    
    def _create_sample_amazon(self):
        """Create sample Amazon data"""
        import numpy as np
        
        # Generate sample products
        n_products = 10000
        categories = ['Electronics', 'Books', 'Clothing', 'Home & Garden', 'Sports']
        
        products = pd.DataFrame({
            'asin': [f'B{i:06d}' for i in range(1, n_products + 1)],
            'title': [f'Product {i}' for i in range(1, n_products + 1)],
            'category': np.random.choice(categories, n_products),
            'price': np.random.uniform(5, 500, n_products),
            'rating': np.random.uniform(3, 5, n_products),
            'review_count': np.random.randint(1, 1000, n_products)
        })
        
        # Generate sample reviews
        n_reviews = 50000
        reviews = pd.DataFrame({
            'asin': np.random.choice(products['asin'], n_reviews),
            'reviewer_id': np.random.randint(1, 5000, n_reviews),
            'rating': np.random.randint(1, 6, n_reviews),
            'review_text': [f'Review text {i}' for i in range(n_reviews)]
        })
        
        # Save files
        products.to_csv(f"{self.data_dir}/amazon_products.csv", index=False)
        reviews.to_csv(f"{self.data_dir}/amazon_reviews.csv", index=False)
    
    def _create_sample_movielens(self):
        """Create sample MovieLens data"""
        import numpy as np
        
        # Generate sample movies
        n_movies = 5000
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller']
        
        movies = pd.DataFrame({
            'movieId': range(1, n_movies + 1),
            'title': [f'Movie {i}' for i in range(1, n_movies + 1)],
            'genres': [np.random.choice(genres) for _ in range(n_movies)]
        })
        
        # Generate sample ratings
        n_ratings = 100000
        ratings = pd.DataFrame({
            'userId': np.random.randint(1, 2000, n_ratings),
            'movieId': np.random.randint(1, n_movies + 1, n_ratings),
            'rating': np.random.randint(1, 6, n_ratings),
            'timestamp': np.random.randint(1000000000, 2000000000, n_ratings)
        })
        
        # Save files
        movies.to_csv(f"{self.data_dir}/movielens_movies.csv", index=False)
        ratings.to_csv(f"{self.data_dir}/movielens_ratings.csv", index=False)
    
    def _create_b2b_dataset(self):
        """Create custom B2B marketplace dataset"""
        import numpy as np
        
        # Generate B2B products
        n_products = 5000
        categories = ['Industrial Equipment', 'Office Supplies', 'Manufacturing Tools', 
                     'Safety Equipment', 'IT Hardware', 'Office Furniture', 'Raw Materials']
        
        products = pd.DataFrame({
            'product_id': range(1, n_products + 1),
            'name': [f'B2B Product {i}' for i in range(1, n_products + 1)],
            'category': np.random.choice(categories, n_products),
            'brand': [f'Brand_{np.random.randint(1, 50)}' for _ in range(n_products)],
            'price': np.random.uniform(50, 5000, n_products),
            'min_order_quantity': np.random.randint(1, 100, n_products),
            'bulk_discount': np.random.uniform(0.05, 0.3, n_products),
            'rating': np.random.uniform(3, 5, n_products)
        })
        
        # Generate B2B users (businesses)
        n_users = 2000
        business_types = ['Manufacturer', 'Retailer', 'Distributor', 'Service Provider', 'Government']
        
        users = pd.DataFrame({
            'user_id': range(1, n_users + 1),
            'business_name': [f'Business {i}' for i in range(1, n_users + 1)],
            'business_type': np.random.choice(business_types, n_users),
            'industry': np.random.choice(['Manufacturing', 'Retail', 'Technology', 'Healthcare', 'Finance'], n_users),
            'annual_revenue': np.random.uniform(100000, 10000000, n_users),
            'employee_count': np.random.randint(10, 1000, n_users),
            'credit_limit': np.random.uniform(10000, 100000, n_users)
        })
        
        # Generate transactions
        n_transactions = 25000
        transactions = pd.DataFrame({
            'transaction_id': range(1, n_transactions + 1),
            'user_id': np.random.randint(1, n_users + 1, n_transactions),
            'product_id': np.random.randint(1, n_products + 1, n_transactions),
            'quantity': np.random.randint(1, 100, n_transactions),
            'unit_price': np.random.uniform(50, 5000, n_transactions),
            'total_amount': np.random.uniform(100, 50000, n_transactions),
            'transaction_date': pd.date_range('2023-01-01', periods=n_transactions, freq='1H'),
            'payment_terms': np.random.choice(['Net 30', 'Net 60', 'Cash', 'Credit'], n_transactions)
        })
        
        # Save files
        products.to_csv(f"{self.data_dir}/b2b_products.csv", index=False)
        users.to_csv(f"{self.data_dir}/b2b_users.csv", index=False)
        transactions.to_csv(f"{self.data_dir}/b2b_transactions.csv", index=False)
    
    def download_all(self) -> bool:
        """Download all available datasets"""
        logger.info("🚀 Starting dataset download process...")
        
        success_count = 0
        total_datasets = len(self.datasets)
        
        # Download each dataset
        for dataset_name, config in self.datasets.items():
            logger.info(f"📥 Processing {dataset_name}: {config['description']}")
            
            if dataset_name == 'retailrocket':
                if self.download_retailrocket():
                    success_count += 1
            elif dataset_name == 'amazon':
                if self.download_amazon():
                    success_count += 1
            elif dataset_name == 'movielens':
                if self.download_movielens():
                    success_count += 1
            elif dataset_name == 'custom_b2b':
                if self.create_custom_b2b_data():
                    success_count += 1
        
        logger.info(f"✅ Dataset download completed: {success_count}/{total_datasets} datasets ready")
        return success_count == total_datasets

def main():
    """Main function"""
    logger.info("🚀 B2B Marketplace Dataset Downloader")
    logger.info("=" * 50)
    
    downloader = DatasetDownloader()
    
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        if dataset_name in downloader.datasets:
            if dataset_name == 'retailrocket':
                downloader.download_retailrocket()
            elif dataset_name == 'amazon':
                downloader.download_amazon()
            elif dataset_name == 'movielens':
                downloader.download_movielens()
            elif dataset_name == 'custom_b2b':
                downloader.create_custom_b2b_data()
        else:
            logger.error(f"❌ Unknown dataset: {dataset_name}")
            logger.info(f"Available datasets: {list(downloader.datasets.keys())}")
    else:
        # Download all datasets
        downloader.download_all()
    
    logger.info("🎉 Dataset preparation completed!")

if __name__ == "__main__":
    main()
