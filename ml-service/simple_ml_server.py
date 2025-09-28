from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json
import os
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for models and data
models = {}
data_cache = {}

class SimpleRecommendationSystem:
    def __init__(self):
        self.models = {}
        self.data_cache = {}
        self.user_item_matrix = None
        self.item_features = None
        self.user_features = None
    
    def generate_sample_data(self):
        """Generate sample B2B e-commerce data"""
        logger.info("Generating sample data...")
        
        np.random.seed(42)
        
        # Generate sample data
        n_users = 500
        n_items = 1000
        n_interactions = 5000
        
        # Create sample events
        events = pd.DataFrame({
            'visitorid': np.random.randint(1, n_users + 1, n_interactions),
            'itemid': np.random.randint(1, n_items + 1, n_interactions),
            'event': np.random.choice(['view', 'addtocart', 'transaction'], n_interactions, p=[0.6, 0.3, 0.1]),
            'timestamp': pd.date_range('2023-01-01', periods=n_interactions, freq='1H')
        })
        
        # Create item properties
        categories = ['Industrial Equipment', 'Office Supplies', 'Manufacturing Tools', 
                     'Safety Equipment', 'IT Hardware', 'Office Furniture']
        
        item_props = []
        for item_id in range(1, n_items + 1):
            item_props.extend([
                {'itemid': item_id, 'property': 'categoryid', 'value': np.random.choice(categories)},
                {'itemid': item_id, 'property': 'brand', 'value': f'Brand_{np.random.randint(1, 10)}'},
                {'itemid': item_id, 'property': 'price', 'value': str(np.random.uniform(10, 500))},
                {'itemid': item_id, 'property': 'rating', 'value': str(np.random.uniform(3, 5))}
            ])
        
        item_properties = pd.DataFrame(item_props)
        
        return events, item_properties
    
    def load_and_preprocess_data(self):
        """Load and preprocess data"""
        cache_key = "preprocessed_data"
        if cache_key in self.data_cache:
            logger.info("Using cached preprocessed data")
            return self.data_cache[cache_key]
        
        logger.info("Loading and preprocessing data...")
        
        # Try to load real data, fallback to generated data
        try:
            events = pd.read_csv('data/events.csv')
            item_properties = pd.read_csv('data/item_properties.csv')
            logger.info("Loaded real data")
        except:
            logger.info("Real data not found, generating sample data...")
            events, item_properties = self.generate_sample_data()
        
        # Preprocess events data
        events['timestamp'] = pd.to_datetime(events['timestamp'])
        
        # Create user-item interaction matrix
        interactions = events.pivot_table(
            index='visitorid', 
            columns='itemid', 
            values='event', 
            aggfunc='count', 
            fill_value=0
        )
        
        # Create binary interaction matrix
        binary_interactions = (interactions > 0).astype(int)
        
        # Extract features from item properties
        item_features = {}
        for _, row in item_properties.iterrows():
            item_id = row['itemid']
            if item_id not in item_features:
                item_features[item_id] = {}
            item_features[item_id][row['property']] = row['value']
        
        # Create user features
        user_features = {}
        for user_id in events['visitorid'].unique():
            user_events = events[events['visitorid'] == user_id]
            user_features[user_id] = {
                'total_events': len(user_events),
                'transaction_count': len(user_events[user_events['event'] == 'transaction']),
                'avg_session_length': user_events.groupby('timestamp').size().mean()
            }
        
        processed_data = {
            'interactions': interactions,
            'binary_interactions': binary_interactions,
            'item_features': item_features,
            'user_features': user_features,
            'events': events,
            'item_properties': item_properties
        }
        
        self.data_cache[cache_key] = processed_data
        return processed_data
    
    def train_content_based_model(self, data):
        """Train content-based recommendation model"""
        logger.info("Training content-based model...")
        
        item_features = data['item_features']
        
        # Create feature matrix for items
        feature_matrix = []
        item_ids = []
        
        for item_id, features in item_features.items():
            feature_vector = []
            
            # Encode categorical features
            category = features.get('categoryid', 'Unknown')
            brand = features.get('brand', 'Unknown')
            price = float(features.get('price', 0))
            rating = float(features.get('rating', 0))
            
            # Simple feature encoding
            feature_vector.extend([
                hash(category) % 100,  # Category hash
                hash(brand) % 50,      # Brand hash
                price / 100,           # Normalized price
                rating                 # Rating
            ])
            
            feature_matrix.append(feature_vector)
            item_ids.append(item_id)
        
        self.models['content_based'] = {
            'feature_matrix': np.array(feature_matrix),
            'item_ids': item_ids,
            'item_features': item_features
        }
        
        logger.info("Content-based model trained successfully")
    
    def train_collaborative_filtering_model(self, data):
        """Train collaborative filtering model"""
        logger.info("Training collaborative filtering model...")
        
        interactions = data['binary_interactions']
        
        # Simple collaborative filtering using cosine similarity
        user_similarity = cosine_similarity(interactions.values)
        
        self.models['collaborative'] = {
            'user_similarity': user_similarity,
            'interactions': interactions,
            'user_ids': interactions.index.tolist()
        }
        
        logger.info("Collaborative filtering model trained successfully")
    
    def get_content_based_recommendations(self, user_id, history, n_recommendations=10):
        """Get content-based recommendations"""
        if 'content_based' not in self.models:
            return []
        
        model = self.models['content_based']
        item_features = model['item_features']
        
        # Get user's preferred features
        user_preferences = []
        for item_id in history:
            if item_id in item_features:
                features = item_features[item_id]
                category = features.get('categoryid', 'Unknown')
                brand = features.get('brand', 'Unknown')
                user_preferences.extend([category, brand])
        
        # Find similar items
        recommendations = []
        for item_id, features in item_features.items():
            if item_id not in history:
                category = features.get('categoryid', 'Unknown')
                brand = features.get('brand', 'Unknown')
                
                # Simple scoring based on user preferences
                score = 0
                if category in user_preferences:
                    score += 0.5
                if brand in user_preferences:
                    score += 0.3
                
                # Add some randomness for variety
                score += np.random.random() * 0.2
                
                if score > 0:
                    recommendations.append((item_id, score))
        
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    def get_collaborative_recommendations(self, user_id, history, n_recommendations=10):
        """Get collaborative filtering recommendations"""
        if 'collaborative' not in self.models:
            return []
        
        model = self.models['collaborative']
        interactions = model['interactions']
        user_similarity = model['user_similarity']
        user_ids = model['user_ids']
        
        if user_id not in user_ids:
            return []
        
        user_idx = user_ids.index(user_id)
        
        # Find similar users
        similar_users = np.argsort(user_similarity[user_idx])[::-1][1:11]  # Top 10 similar users
        
        # Get items liked by similar users
        item_scores = {}
        for similar_user_idx in similar_users:
            similar_user_id = user_ids[similar_user_idx]
            similarity_score = user_similarity[user_idx, similar_user_idx]
            
            # Get items liked by this user
            user_items = interactions.loc[similar_user_id]
            liked_items = user_items[user_items > 0].index.tolist()
            
            for item_id in liked_items:
                if item_id not in history:
                    if item_id not in item_scores:
                        item_scores[item_id] = 0
                    item_scores[item_id] += similarity_score
        
        # Convert to list and sort
        recommendations = [(item_id, score) for item_id, score in item_scores.items()]
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    def get_hybrid_recommendations(self, user_id, history, n_recommendations=10):
        """Get hybrid recommendations combining multiple approaches"""
        logger.info(f"Getting hybrid recommendations for user {user_id}")
        
        # Get recommendations from different models
        content_recs = self.get_content_based_recommendations(user_id, history, n_recommendations * 2)
        collab_recs = self.get_collaborative_recommendations(user_id, history, n_recommendations * 2)
        
        # Combine recommendations with weights
        all_recommendations = {}
        
        # Content-based recommendations (weight: 0.6)
        for item_id, score in content_recs:
            if item_id not in all_recommendations:
                all_recommendations[item_id] = 0
            all_recommendations[item_id] += score * 0.6
        
        # Collaborative filtering recommendations (weight: 0.4)
        for item_id, score in collab_recs:
            if item_id not in all_recommendations:
                all_recommendations[item_id] = 0
            all_recommendations[item_id] += score * 0.4
        
        # Sort by combined score
        combined_recommendations = sorted(all_recommendations.items(), key=lambda x: x[1], reverse=True)
        
        return combined_recommendations[:n_recommendations]
    
    def get_explanation(self, user_id, item_id, recommendation_score):
        """Generate explanation for recommendation"""
        explanations = [
            f"Based on your purchase history, this item has a {recommendation_score:.1%} match score.",
            f"Similar users who bought items like yours also purchased this product.",
            f"This item is frequently bought together with items in your cart.",
            f"Based on your preferences and browsing history, this is a highly recommended item.",
            f"This product matches your business needs with a {recommendation_score:.1%} confidence score."
        ]
        
        # Select explanation based on score
        if recommendation_score > 0.8:
            return explanations[0]
        elif recommendation_score > 0.6:
            return explanations[1]
        elif recommendation_score > 0.4:
            return explanations[2]
        else:
            return explanations[3]

# Initialize the recommendation system
rec_system = SimpleRecommendationSystem()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': list(rec_system.models.keys()),
        'service': 'Simple ML Recommendation Service'
    })

@app.route('/train', methods=['POST'])
def train_models():
    """Train all recommendation models"""
    try:
        logger.info("Starting model training...")
        
        # Load and preprocess data
        data = rec_system.load_and_preprocess_data()
        
        # Train models
        rec_system.train_content_based_model(data)
        rec_system.train_collaborative_filtering_model(data)
        
        return jsonify({
            'status': 'success',
            'message': 'All models trained successfully',
            'models': list(rec_system.models.keys())
        })
    
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Get hybrid recommendations"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        history = data.get('history', [])
        n_recommendations = data.get('n_recommendations', 10)
        
        # Get hybrid recommendations
        recommendations = rec_system.get_hybrid_recommendations(
            user_id, history, n_recommendations
        )
        
        # Format response
        formatted_recs = []
        for item_id, score in recommendations:
            explanation = rec_system.get_explanation(user_id, item_id, score)
            formatted_recs.append({
                'product': f'Product_{item_id}',
                'score': float(score),
                'sim': float(score),  # For compatibility
                'reason': explanation
            })
        
        return jsonify({'recommendations': formatted_recs})
    
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """Get recommendations for a specific user"""
    try:
        # Get user history (this would come from database in production)
        history = []  # Placeholder
        
        recommendations = rec_system.get_hybrid_recommendations(user_id, history, 10)
        
        formatted_recs = []
        for item_id, score in recommendations:
            explanation = rec_system.get_explanation(user_id, item_id, score)
            formatted_recs.append({
                'product': f'Product_{item_id}',
                'score': float(score),
                'reason': explanation
            })
        
        return jsonify({'recommendations': formatted_recs})
    
    except Exception as e:
        logger.error(f"Failed to get recommendations: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get model performance analytics"""
    try:
        analytics = {
            'models_loaded': list(rec_system.models.keys()),
            'service': 'Simple ML Recommendation Service',
            'timestamp': datetime.now().isoformat(),
            'status': 'operational'
        }
        
        return jsonify(analytics)
    
    except Exception as e:
        logger.error(f"Failed to get analytics: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting Simple ML Recommendation Service...")
    app.run(host='0.0.0.0', port=5001, debug=True)
