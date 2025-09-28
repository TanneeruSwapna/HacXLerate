#!/usr/bin/env python3
"""
Train ML models with large datasets for B2B recommendations
"""

import os
import sys
import yaml
import logging
import argparse
from typing import Dict, Any
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.neural_collaborative import NeuralCollaborativeFiltering
from core.content_based import ContentBasedRecommender
from core.collaborative_filtering import CollaborativeFilteringRecommender
from core.hybrid_recommender import HybridRecommender

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Train ML models with large datasets"""
    
    def __init__(self, config_path: str = "configs/training_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.models = {}
        self.data = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load training configuration"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"✅ Loaded configuration from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"⚠️ Config file not found: {self.config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default training configuration"""
        return {
            'data': {
                'dataset': 'custom_b2b',
                'batch_size': 1024,
                'validation_split': 0.2
            },
            'models': {
                'neural_collaborative': {
                    'embedding_dim': 50,
                    'hidden_layers': [128, 64, 32],
                    'learning_rate': 0.001,
                    'epochs': 100,
                    'batch_size': 1024
                },
                'content_based': {
                    'similarity_threshold': 0.7,
                    'feature_weights': {
                        'category': 0.4,
                        'brand': 0.3,
                        'price': 0.2,
                        'rating': 0.1
                    }
                },
                'collaborative_filtering': {
                    'similarity_metric': 'cosine',
                    'min_similarity': 0.1,
                    'max_neighbors': 50
                }
            },
            'training': {
                'save_models': True,
                'model_dir': 'models/checkpoints',
                'evaluate_models': True
            }
        }
    
    def load_data(self) -> bool:
        """Load training data"""
        logger.info("📊 Loading training data...")
        
        dataset_name = self.config['data']['dataset']
        data_dir = f"data/datasets"
        
        try:
            if dataset_name == 'custom_b2b':
                self._load_b2b_data(data_dir)
            elif dataset_name == 'retailrocket':
                self._load_retailrocket_data(data_dir)
            elif dataset_name == 'amazon':
                self._load_amazon_data(data_dir)
            elif dataset_name == 'movielens':
                self._load_movielens_data(data_dir)
            else:
                logger.error(f"❌ Unknown dataset: {dataset_name}")
                return False
            
            logger.info("✅ Data loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load data: {e}")
            return False
    
    def _load_b2b_data(self, data_dir: str):
        """Load B2B dataset"""
        products = pd.read_csv(f"{data_dir}/b2b_products.csv")
        users = pd.read_csv(f"{data_dir}/b2b_users.csv")
        transactions = pd.read_csv(f"{data_dir}/b2b_transactions.csv")
        
        # Create interactions matrix
        interactions = {}
        for _, row in transactions.iterrows():
            user_id = row['user_id']
            product_id = row['product_id']
            quantity = row['quantity']
            
            if user_id not in interactions:
                interactions[user_id] = {}
            interactions[user_id][product_id] = quantity
        
        # Create item features
        item_features = {}
        for _, row in products.iterrows():
            item_id = row['product_id']
            item_features[item_id] = {
                'category': row['category'],
                'brand': row['brand'],
                'price': row['price'],
                'rating': row['rating'],
                'min_order_quantity': row['min_order_quantity'],
                'bulk_discount': row['bulk_discount']
            }
        
        # Create user features
        user_features = {}
        for _, row in users.iterrows():
            user_id = row['user_id']
            user_features[user_id] = {
                'business_type': row['business_type'],
                'industry': row['industry'],
                'annual_revenue': row['annual_revenue'],
                'employee_count': row['employee_count'],
                'credit_limit': row['credit_limit']
            }
        
        self.data = {
            'interactions': interactions,
            'item_features': item_features,
            'user_features': user_features,
            'products': products,
            'users': users,
            'transactions': transactions
        }
    
    def _load_retailrocket_data(self, data_dir: str):
        """Load Retailrocket dataset"""
        events = pd.read_csv(f"{data_dir}/retailrocket_events.csv")
        item_properties = pd.read_csv(f"{data_dir}/retailrocket_item_properties.csv")
        
        # Process events
        interactions = {}
        for _, row in events.iterrows():
            user_id = row['visitorid']
            item_id = row['itemid']
            event = row['event']
            
            if user_id not in interactions:
                interactions[user_id] = {}
            
            # Weight events
            weight = {'view': 1, 'addtocart': 3, 'transaction': 5}
            if item_id not in interactions[user_id]:
                interactions[user_id][item_id] = 0
            interactions[user_id][item_id] += weight.get(event, 1)
        
        # Process item properties
        item_features = {}
        for _, row in item_properties.iterrows():
            item_id = row['itemid']
            property_name = row['property']
            value = row['value']
            
            if item_id not in item_features:
                item_features[item_id] = {}
            item_features[item_id][property_name] = value
        
        self.data = {
            'interactions': interactions,
            'item_features': item_features,
            'user_features': {},
            'events': events,
            'item_properties': item_properties
        }
    
    def _load_amazon_data(self, data_dir: str):
        """Load Amazon dataset"""
        products = pd.read_csv(f"{data_dir}/amazon_products.csv")
        reviews = pd.read_csv(f"{data_dir}/amazon_reviews.csv")
        
        # Create interactions from reviews
        interactions = {}
        for _, row in reviews.iterrows():
            user_id = row['reviewer_id']
            item_id = row['asin']
            rating = row['rating']
            
            if user_id not in interactions:
                interactions[user_id] = {}
            interactions[user_id][item_id] = rating
        
        # Create item features
        item_features = {}
        for _, row in products.iterrows():
            item_id = row['asin']
            item_features[item_id] = {
                'category': row['category'],
                'price': row['price'],
                'rating': row['rating'],
                'review_count': row['review_count']
            }
        
        self.data = {
            'interactions': interactions,
            'item_features': item_features,
            'user_features': {},
            'products': products,
            'reviews': reviews
        }
    
    def _load_movielens_data(self, data_dir: str):
        """Load MovieLens dataset"""
        movies = pd.read_csv(f"{data_dir}/movielens_movies.csv")
        ratings = pd.read_csv(f"{data_dir}/movielens_ratings.csv")
        
        # Create interactions from ratings
        interactions = {}
        for _, row in ratings.iterrows():
            user_id = row['userId']
            item_id = row['movieId']
            rating = row['rating']
            
            if user_id not in interactions:
                interactions[user_id] = {}
            interactions[user_id][item_id] = rating
        
        # Create item features
        item_features = {}
        for _, row in movies.iterrows():
            item_id = row['movieId']
            item_features[item_id] = {
                'title': row['title'],
                'genres': row['genres']
            }
        
        self.data = {
            'interactions': interactions,
            'item_features': item_features,
            'user_features': {},
            'movies': movies,
            'ratings': ratings
        }
    
    def train_models(self) -> bool:
        """Train all configured models"""
        logger.info("🚀 Starting model training...")
        
        # Create models directory
        os.makedirs(self.config['training']['model_dir'], exist_ok=True)
        
        # Train Neural Collaborative Filtering
        if 'neural_collaborative' in self.config['models']:
            logger.info("🧠 Training Neural Collaborative Filtering...")
            try:
                ncf = NeuralCollaborativeFiltering(self.config['models']['neural_collaborative'])
                ncf.train(self.data)
                self.models['neural_collaborative'] = ncf
                
                if self.config['training']['save_models']:
                    model_path = f"{self.config['training']['model_dir']}/ncf_model.pth"
                    ncf.save_model(model_path)
                    logger.info(f"✅ NCF model saved to {model_path}")
                
            except Exception as e:
                logger.error(f"❌ NCF training failed: {e}")
        
        # Train Content-Based Recommender
        if 'content_based' in self.config['models']:
            logger.info("📝 Training Content-Based Recommender...")
            try:
                cb = ContentBasedRecommender(self.config['models']['content_based'])
                cb.train(self.data)
                self.models['content_based'] = cb
                
                if self.config['training']['save_models']:
                    model_path = f"{self.config['training']['model_dir']}/content_based_model.pkl"
                    cb.save_model(model_path)
                    logger.info(f"✅ Content-Based model saved to {model_path}")
                
            except Exception as e:
                logger.error(f"❌ Content-Based training failed: {e}")
        
        # Train Collaborative Filtering
        if 'collaborative_filtering' in self.config['models']:
            logger.info("👥 Training Collaborative Filtering...")
            try:
                cf = CollaborativeFilteringRecommender(self.config['models']['collaborative_filtering'])
                cf.train(self.data)
                self.models['collaborative_filtering'] = cf
                
                if self.config['training']['save_models']:
                    model_path = f"{self.config['training']['model_dir']}/collaborative_filtering_model.pkl"
                    cf.save_model(model_path)
                    logger.info(f"✅ Collaborative Filtering model saved to {model_path}")
                
            except Exception as e:
                logger.error(f"❌ Collaborative Filtering training failed: {e}")
        
        # Train Hybrid Recommender
        logger.info("🔀 Training Hybrid Recommender...")
        try:
            hybrid = HybridRecommender({
                'models': list(self.models.keys()),
                'weights': {'neural_collaborative': 0.4, 'content_based': 0.3, 'collaborative_filtering': 0.3}
            })
            hybrid.train(self.data)
            self.models['hybrid'] = hybrid
            
            if self.config['training']['save_models']:
                model_path = f"{self.config['training']['model_dir']}/hybrid_model.pkl"
                hybrid.save_model(model_path)
                logger.info(f"✅ Hybrid model saved to {model_path}")
            
        except Exception as e:
            logger.error(f"❌ Hybrid training failed: {e}")
        
        logger.info(f"✅ Model training completed: {len(self.models)} models trained")
        return True
    
    def evaluate_models(self) -> Dict[str, Dict[str, float]]:
        """Evaluate all trained models"""
        if not self.config['training']['evaluate_models']:
            return {}
        
        logger.info("📊 Evaluating models...")
        
        # Split data for evaluation
        test_data = self._split_data_for_evaluation()
        
        results = {}
        for model_name, model in self.models.items():
            try:
                metrics = model.evaluate(test_data)
                results[model_name] = metrics
                logger.info(f"✅ {model_name} evaluation completed")
            except Exception as e:
                logger.error(f"❌ {model_name} evaluation failed: {e}")
                results[model_name] = {}
        
        return results
    
    def _split_data_for_evaluation(self) -> Dict[str, Any]:
        """Split data for model evaluation"""
        # Simple train/test split for evaluation
        interactions = self.data['interactions']
        test_interactions = {}
        
        for user_id, items in interactions.items():
            if len(items) > 1:  # Only users with multiple interactions
                # Keep 80% for training, 20% for testing
                item_list = list(items.items())
                test_size = max(1, len(item_list) // 5)
                test_items = dict(item_list[:test_size])
                test_interactions[user_id] = test_items
        
        return {
            'interactions': test_interactions,
            'item_features': self.data['item_features'],
            'user_features': self.data['user_features']
        }
    
    def save_training_results(self, results: Dict[str, Dict[str, float]]):
        """Save training results"""
        results_file = f"{self.config['training']['model_dir']}/training_results.yaml"
        
        with open(results_file, 'w') as file:
            yaml.dump(results, file, default_flow_style=False)
        
        logger.info(f"📊 Training results saved to {results_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Train ML models for B2B recommendations')
    parser.add_argument('--config', default='configs/training_config.yaml', help='Training configuration file')
    parser.add_argument('--dataset', help='Dataset to use (overrides config)')
    parser.add_argument('--models', nargs='+', help='Models to train')
    
    args = parser.parse_args()
    
    logger.info("🚀 B2B Marketplace Model Training")
    logger.info("=" * 50)
    
    trainer = ModelTrainer(args.config)
    
    # Override config if specified
    if args.dataset:
        trainer.config['data']['dataset'] = args.dataset
    
    # Load data
    if not trainer.load_data():
        logger.error("❌ Failed to load data")
        sys.exit(1)
    
    # Train models
    if not trainer.train_models():
        logger.error("❌ Model training failed")
        sys.exit(1)
    
    # Evaluate models
    results = trainer.evaluate_models()
    
    # Save results
    trainer.save_training_results(results)
    
    logger.info("🎉 Model training completed successfully!")

if __name__ == "__main__":
    main()
