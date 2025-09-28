#!/usr/bin/env python3
"""
Evaluate ML models for B2B recommendations
"""

import os
import sys
import yaml
import logging
import argparse
from typing import Dict, Any
import pandas as pd
import numpy as np
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.neural_collaborative import NeuralCollaborativeFiltering
from core.content_based import ContentBasedRecommender
from core.collaborative_filtering import CollaborativeFilteringRecommender
from core.hybrid_recommender import HybridRecommender

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Evaluate ML models for B2B recommendations"""
    
    def __init__(self, config_path: str = "configs/training_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.models = {}
        self.data = {}
        self.results = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load evaluation configuration"""
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"✅ Loaded configuration from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"⚠️ Config file not found: {self.config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default evaluation configuration"""
        return {
            'evaluation': {
                'metrics': ['precision@10', 'recall@10', 'ndcg@10', 'map@10', 'coverage', 'diversity'],
                'test_split': 0.2,
                'cross_validation': False,
                'cv_folds': 5
            },
            'models': {
                'neural_collaborative': {'enabled': True},
                'content_based': {'enabled': True},
                'collaborative_filtering': {'enabled': True},
                'hybrid': {'enabled': True}
            }
        }
    
    def load_data(self) -> bool:
        """Load test data"""
        logger.info("📊 Loading test data...")
        
        try:
            # Load B2B dataset
            data_dir = "data/datasets"
            
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
                    'rating': row['rating']
                }
            
            # Create user features
            user_features = {}
            for _, row in users.iterrows():
                user_id = row['user_id']
                user_features[user_id] = {
                    'business_type': row['business_type'],
                    'industry': row['industry'],
                    'annual_revenue': row['annual_revenue']
                }
            
            self.data = {
                'interactions': interactions,
                'item_features': item_features,
                'user_features': user_features
            }
            
            logger.info("✅ Test data loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load test data: {e}")
            return False
    
    def load_models(self) -> bool:
        """Load trained models"""
        logger.info("🤖 Loading trained models...")
        
        model_dir = "models/checkpoints"
        
        try:
            # Load Neural Collaborative Filtering
            if self.config['models']['neural_collaborative']['enabled']:
                ncf = NeuralCollaborativeFiltering()
                ncf.load_model(f"{model_dir}/ncf_model.pth")
                self.models['neural_collaborative'] = ncf
                logger.info("✅ NCF model loaded")
            
            # Load Content-Based Recommender
            if self.config['models']['content_based']['enabled']:
                cb = ContentBasedRecommender()
                cb.load_model(f"{model_dir}/content_based_model.pkl")
                self.models['content_based'] = cb
                logger.info("✅ Content-Based model loaded")
            
            # Load Collaborative Filtering
            if self.config['models']['collaborative_filtering']['enabled']:
                cf = CollaborativeFilteringRecommender()
                cf.load_model(f"{model_dir}/collaborative_filtering_model.pkl")
                self.models['collaborative_filtering'] = cf
                logger.info("✅ Collaborative Filtering model loaded")
            
            # Load Hybrid Recommender
            if self.config['models']['hybrid']['enabled']:
                hybrid = HybridRecommender()
                hybrid.load_model(f"{model_dir}/hybrid_model.pkl")
                self.models['hybrid'] = hybrid
                logger.info("✅ Hybrid model loaded")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
            return False
    
    def evaluate_models(self) -> Dict[str, Dict[str, float]]:
        """Evaluate all models"""
        logger.info("📊 Evaluating models...")
        
        # Split data for evaluation
        test_data = self._split_data_for_evaluation()
        
        results = {}
        for model_name, model in self.models.items():
            logger.info(f"🔍 Evaluating {model_name}...")
            try:
                metrics = model.evaluate(test_data)
                results[model_name] = metrics
                logger.info(f"✅ {model_name} evaluation completed")
            except Exception as e:
                logger.error(f"❌ {model_name} evaluation failed: {e}")
                results[model_name] = {}
        
        self.results = results
        return results
    
    def _split_data_for_evaluation(self) -> Dict[str, Any]:
        """Split data for model evaluation"""
        interactions = self.data['interactions']
        test_interactions = {}
        
        for user_id, items in interactions.items():
            if len(items) > 1:  # Only users with multiple interactions
                # Keep 20% for testing
                item_list = list(items.items())
                test_size = max(1, len(item_list) // 5)
                test_items = dict(item_list[:test_size])
                test_interactions[user_id] = test_items
        
        return {
            'interactions': test_interactions,
            'item_features': self.data['item_features'],
            'user_features': self.data['user_features']
        }
    
    def calculate_additional_metrics(self) -> Dict[str, Dict[str, float]]:
        """Calculate additional evaluation metrics"""
        logger.info("📈 Calculating additional metrics...")
        
        additional_metrics = {}
        
        for model_name, model in self.models.items():
            logger.info(f"🔍 Calculating additional metrics for {model_name}...")
            
            try:
                # Calculate coverage
                coverage = self._calculate_coverage(model_name)
                
                # Calculate diversity
                diversity = self._calculate_diversity(model_name)
                
                # Calculate novelty
                novelty = self._calculate_novelty(model_name)
                
                additional_metrics[model_name] = {
                    'coverage': coverage,
                    'diversity': diversity,
                    'novelty': novelty
                }
                
            except Exception as e:
                logger.error(f"❌ Additional metrics calculation failed for {model_name}: {e}")
                additional_metrics[model_name] = {}
        
        return additional_metrics
    
    def _calculate_coverage(self, model_name: str) -> float:
        """Calculate model coverage"""
        # Coverage: percentage of items that can be recommended
        total_items = len(self.data['item_features'])
        recommended_items = set()
        
        # Sample users for coverage calculation
        sample_users = list(self.data['interactions'].keys())[:100]
        
        for user_id in sample_users:
            try:
                recommendations = self.models[model_name].predict(user_id, [], n_recommendations=10)
                for item_id, _ in recommendations:
                    recommended_items.add(item_id)
            except:
                continue
        
        coverage = len(recommended_items) / total_items if total_items > 0 else 0.0
        return coverage
    
    def _calculate_diversity(self, model_name: str) -> float:
        """Calculate recommendation diversity"""
        # Diversity: average pairwise distance between recommended items
        diversities = []
        
        # Sample users for diversity calculation
        sample_users = list(self.data['interactions'].keys())[:50]
        
        for user_id in sample_users:
            try:
                recommendations = self.models[model_name].predict(user_id, [], n_recommendations=10)
                if len(recommendations) > 1:
                    # Calculate diversity based on item categories
                    categories = []
                    for item_id, _ in recommendations:
                        if item_id in self.data['item_features']:
                            categories.append(self.data['item_features'][item_id]['category'])
                    
                    # Calculate category diversity
                    unique_categories = len(set(categories))
                    total_categories = len(categories)
                    diversity = unique_categories / total_categories if total_categories > 0 else 0.0
                    diversities.append(diversity)
            except:
                continue
        
        return np.mean(diversities) if diversities else 0.0
    
    def _calculate_novelty(self, model_name: str) -> float:
        """Calculate recommendation novelty"""
        # Novelty: average popularity of recommended items (inverse)
        novelties = []
        
        # Calculate item popularity
        item_popularity = {}
        for user_id, items in self.data['interactions'].items():
            for item_id in items.keys():
                item_popularity[item_id] = item_popularity.get(item_id, 0) + 1
        
        # Sample users for novelty calculation
        sample_users = list(self.data['interactions'].keys())[:50]
        
        for user_id in sample_users:
            try:
                recommendations = self.models[model_name].predict(user_id, [], n_recommendations=10)
                if recommendations:
                    # Calculate average popularity of recommended items
                    avg_popularity = np.mean([item_popularity.get(item_id, 0) for item_id, _ in recommendations])
                    # Convert to novelty (lower popularity = higher novelty)
                    max_popularity = max(item_popularity.values()) if item_popularity else 1
                    novelty = 1 - (avg_popularity / max_popularity)
                    novelties.append(novelty)
            except:
                continue
        
        return np.mean(novelties) if novelties else 0.0
    
    def generate_report(self) -> str:
        """Generate evaluation report"""
        logger.info("📝 Generating evaluation report...")
        
        report = []
        report.append("# B2B Marketplace ML Models Evaluation Report")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Model performance comparison
        report.append("## Model Performance Comparison")
        report.append("")
        
        # Create comparison table
        metrics = ['precision@10', 'recall@10', 'ndcg@10', 'coverage', 'diversity', 'novelty']
        
        # Header
        header = "| Model | " + " | ".join(metrics) + " |"
        report.append(header)
        report.append("|" + "|".join(["---"] * (len(metrics) + 1)) + "|")
        
        # Results for each model
        for model_name, metrics_dict in self.results.items():
            row = f"| {model_name} |"
            for metric in metrics:
                value = metrics_dict.get(metric, 0.0)
                row += f" {value:.4f} |"
            report.append(row)
        
        report.append("")
        
        # Detailed results
        report.append("## Detailed Results")
        report.append("")
        
        for model_name, metrics_dict in self.results.items():
            report.append(f"### {model_name}")
            report.append("")
            
            for metric, value in metrics_dict.items():
                report.append(f"- **{metric}**: {value:.4f}")
            
            report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        report.append("")
        
        # Find best model for each metric
        best_models = {}
        for metric in metrics:
            best_model = None
            best_value = 0.0
            
            for model_name, metrics_dict in self.results.items():
                value = metrics_dict.get(metric, 0.0)
                if value > best_value:
                    best_value = value
                    best_model = model_name
            
            if best_model:
                best_models[metric] = best_model
        
        report.append("### Best Models by Metric:")
        for metric, model in best_models.items():
            report.append(f"- **{metric}**: {model}")
        
        report.append("")
        report.append("### Overall Recommendation:")
        
        # Calculate overall score
        overall_scores = {}
        for model_name, metrics_dict in self.results.items():
            score = 0.0
            count = 0
            for metric, value in metrics_dict.items():
                if metric in ['precision@10', 'recall@10', 'ndcg@10']:
                    score += value
                    count += 1
            overall_scores[model_name] = score / count if count > 0 else 0.0
        
        best_overall = max(overall_scores.items(), key=lambda x: x[1])
        report.append(f"**{best_overall[0]}** is the best overall performing model with a score of {best_overall[1]:.4f}")
        
        return "\n".join(report)
    
    def save_results(self, results: Dict[str, Dict[str, float]]):
        """Save evaluation results"""
        # Save as JSON
        results_file = "models/evaluation_results.json"
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"📊 Results saved to {results_file}")
        
        # Save as YAML
        yaml_file = "models/evaluation_results.yaml"
        with open(yaml_file, 'w') as f:
            yaml.dump(results, f, default_flow_style=False)
        
        logger.info(f"📊 Results saved to {yaml_file}")
        
        # Save report
        report = self.generate_report()
        report_file = "models/evaluation_report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"📝 Report saved to {report_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Evaluate ML models for B2B recommendations')
    parser.add_argument('--config', default='configs/training_config.yaml', help='Evaluation configuration file')
    parser.add_argument('--models', nargs='+', help='Models to evaluate')
    parser.add_argument('--output', default='models/evaluation_results.json', help='Output file')
    
    args = parser.parse_args()
    
    logger.info("🚀 B2B Marketplace Model Evaluation")
    logger.info("=" * 50)

    evaluator = ModelEvaluator(args.config)
    
    # Load test data
    if not evaluator.load_data():
        logger.error("❌ Failed to load test data")
        sys.exit(1)
    
    # Load trained models
    if not evaluator.load_models():
        logger.error("❌ Failed to load models")
        sys.exit(1)
    
    # Evaluate models
    results = evaluator.evaluate_models()
    
    # Calculate additional metrics
    additional_metrics = evaluator.calculate_additional_metrics()
    
    # Merge results
    for model_name in results:
        if model_name in additional_metrics:
            results[model_name].update(additional_metrics[model_name])
    
    # Save results
    evaluator.save_results(results)
    
    # Print summary
    logger.info("📊 Evaluation Summary:")
    for model_name, metrics in results.items():
        logger.info(f"  {model_name}:")
        for metric, value in metrics.items():
            logger.info(f"    {metric}: {value:.4f}")
    
    logger.info("🎉 Model evaluation completed successfully!")

if __name__ == "__main__":
    main()
