from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import xgboost as xgb
from lightfm import LightFM
from lightfm.data import Dataset as LightFMDataset
from lightfm.evaluation import precision_at_k, recall_at_k
from sentence_transformers import SentenceTransformer
import implicit
import redis
import json
import pickle
import os
from datetime import datetime, timedelta
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
redis_client = None

class AdvancedRecommendationSystem:
    def __init__(self):
        self.models = {}
        self.data_cache = {}
        self.redis_client = None
        self.sentence_transformer = None
        self.setup_redis()
        self.load_sentence_transformer()
    
    def setup_redis(self):
        """Setup Redis for caching"""
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_client.ping()
            logger.info("Redis connected successfully")
        except:
            logger.warning("Redis not available, using in-memory cache")
            self.redis_client = None
    
    def load_sentence_transformer(self):
        """Load sentence transformer for text embeddings"""
        try:
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load sentence transformer: {e}")
            self.sentence_transformer = None
    
    def cache_get(self, key: str):
        """Get data from cache"""
        if self.redis_client:
            try:
                data = self.redis_client.get(key)
                return json.loads(data) if data else None
            except:
                return None
        return self.data_cache.get(key)
    
    def cache_set(self, key: str, data, expire: int = 3600):
        """Set data in cache"""
        if self.redis_client:
            try:
                self.redis_client.setex(key, expire, json.dumps(data, default=str))
            except:
                pass
        self.data_cache[key] = data
    
    def load_and_preprocess_data(self):
        """Load and preprocess data for multiple algorithms"""
        cache_key = "preprocessed_data"
        cached_data = self.cache_get(cache_key)
        if cached_data:
            logger.info("Using cached preprocessed data")
            return cached_data
        
        logger.info("Loading and preprocessing data...")
        
        # Try to load real data, fallback to generated data
        try:
            events = pd.read_csv('data/events.csv')
            item_props = pd.read_csv('data/item_properties.csv')
            logger.info("Loaded real Retailrocket data")
        except:
            logger.info("Real data not found, generating synthetic data...")
            events, item_props = self.generate_synthetic_data()
        
        # Preprocess events data
        events['timestamp'] = pd.to_datetime(events['timestamp'])
        events = events.sort_values('timestamp')
        
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
        item_features = self.extract_item_features(item_props)
        
        # Create user features
        user_features = self.extract_user_features(events)
        
        # Prepare data for different algorithms
        processed_data = {
            'interactions': interactions,
            'binary_interactions': binary_interactions,
            'item_features': item_features,
            'user_features': user_features,
            'events': events,
            'item_props': item_props
        }
        
        self.cache_set(cache_key, processed_data, expire=7200)  # Cache for 2 hours
        return processed_data
    
    def generate_synthetic_data(self):
        """Generate synthetic data for testing"""
        np.random.seed(42)
        
        # Generate events
        n_events = 50000
        n_users = 1000
        n_items = 2000
        
        events = pd.DataFrame({
            'visitorid': np.random.randint(1, n_users + 1, n_events),
            'itemid': np.random.randint(1, n_items + 1, n_events),
            'event': np.random.choice(['view', 'addtocart', 'transaction'], n_events, p=[0.6, 0.3, 0.1]),
            'timestamp': pd.date_range('2023-01-01', periods=n_events, freq='1H')
        })
        
        # Generate item properties
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
        brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
        
        item_props = []
        for item_id in range(1, n_items + 1):
            item_props.extend([
                {'itemid': item_id, 'property': 'categoryid', 'value': np.random.choice(categories)},
                {'itemid': item_id, 'property': 'brand', 'value': np.random.choice(brands)},
                {'itemid': item_id, 'property': 'price', 'value': np.random.uniform(10, 500)},
                {'itemid': item_id, 'property': 'rating', 'value': np.random.uniform(3, 5)}
            ])
        
        item_props = pd.DataFrame(item_props)
        
        return events, item_props
    
    def extract_item_features(self, item_props):
        """Extract features from item properties"""
        features = {}
        
        for _, row in item_props.iterrows():
            item_id = row['itemid']
            if item_id not in features:
                features[item_id] = {}
            features[item_id][row['property']] = row['value']
        
        return features
    
    def extract_user_features(self, events):
        """Extract user features from events"""
        user_features = {}
        
        for user_id in events['visitorid'].unique():
            user_events = events[events['visitorid'] == user_id]
            user_features[user_id] = {
                'total_events': len(user_events),
                'transaction_count': len(user_events[user_events['event'] == 'transaction']),
                'avg_session_length': user_events.groupby('timestamp').size().mean(),
                'preferred_categories': user_events['itemid'].value_counts().head(5).to_dict()
            }
        
        return user_features
    
    def train_neural_collaborative_filtering(self, data):
        """Train Neural Collaborative Filtering model"""
        logger.info("Training Neural Collaborative Filtering model...")
        
        interactions = data['binary_interactions']
        
        # Create user and item mappings
        user_to_idx = {u: i for i, u in enumerate(interactions.index)}
        item_to_idx = {i: j for j, i in enumerate(interactions.columns)}
        
        # Convert to numpy array
        interaction_matrix = interactions.values
        
        # Split data
        train_data, test_data = train_test_split(interaction_matrix, test_size=0.2, random_state=42)
        
        # Create PyTorch dataset
        class NCFDataset(Dataset):
            def __init__(self, matrix):
                self.users, self.items = np.where(matrix > 0)
                self.ratings = matrix[self.users, self.items]
                
            def __len__(self):
                return len(self.users)
            
            def __getitem__(self, idx):
                return self.users[idx], self.items[idx], self.ratings[idx]
        
        train_dataset = NCFDataset(train_data)
        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
        
        # Define NCF model
        class AdvancedNCF(nn.Module):
            def __init__(self, num_users, num_items, embedding_size=64):
                super().__init__()
                self.user_emb = nn.Embedding(num_users, embedding_size)
                self.item_emb = nn.Embedding(num_items, embedding_size)
                self.fc = nn.Sequential(
                    nn.Linear(embedding_size * 2, 256),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(128, 64),
                    nn.ReLU(),
                    nn.Linear(64, 1),
                    nn.Sigmoid()
                )
            
            def forward(self, user, item):
                u = self.user_emb(user)
                i = self.item_emb(item)
                x = torch.cat([u, i], dim=1)
                return self.fc(x)
        
        # Initialize model
        model = AdvancedNCF(len(user_to_idx), len(item_to_idx))
        optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
        criterion = nn.BCELoss()
        
        # Training loop
        model.train()
        for epoch in range(50):
            total_loss = 0
            for u, i, r in train_loader:
                u, i, r = u.long(), i.long(), r.float().unsqueeze(1)
                optimizer.zero_grad()
                pred = model(u, i)
                loss = criterion(pred, r)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            if epoch % 10 == 0:
                logger.info(f'NCF Epoch {epoch+1}, Loss: {total_loss / len(train_loader):.4f}')
        
        # Store model and mappings
        self.models['ncf'] = {
            'model': model,
            'user_to_idx': user_to_idx,
            'item_to_idx': item_to_idx,
            'interaction_matrix': interaction_matrix
        }
        
        logger.info("Neural Collaborative Filtering model trained successfully")
    
    def train_lightfm_model(self, data):
        """Train LightFM model for hybrid recommendations"""
        logger.info("Training LightFM model...")
        
        interactions = data['binary_interactions']
        item_features = data['item_features']
        
        # Prepare data for LightFM
        dataset = LightFMDataset()
        dataset.fit(
            users=interactions.index,
            items=interactions.columns,
            item_features=[(item_id, props) for item_id, props in item_features.items()]
        )
        
        # Build interaction matrix
        (interactions_matrix, weights) = dataset.build_interactions(
            [(row.name, col, 1) for row in interactions.itertuples() for col in interactions.columns if row[col] > 0]
        )
        
        # Build item features
        item_features_matrix = dataset.build_item_features(
            [(item_id, props) for item_id, props in item_features.items()]
        )
        
        # Train model
        model = LightFM(no_components=50, learning_rate=0.05, loss='warp')
        model.fit(interactions_matrix, item_features=item_features_matrix, epochs=30, num_threads=4)
        
        self.models['lightfm'] = {
            'model': model,
            'dataset': dataset,
            'interactions_matrix': interactions_matrix
        }
        
        logger.info("LightFM model trained successfully")
    
    def train_xgboost_model(self, data):
        """Train XGBoost model for content-based recommendations"""
        logger.info("Training XGBoost model...")
        
        # Prepare features
        features = []
        labels = []
        
        for user_id in data['binary_interactions'].index:
            for item_id in data['binary_interactions'].columns:
                # User features
                user_feat = data['user_features'].get(user_id, {})
                
                # Item features
                item_feat = data['item_features'].get(item_id, {})
                
                # Create feature vector
                feature_vector = [
                    user_feat.get('total_events', 0),
                    user_feat.get('transaction_count', 0),
                    user_feat.get('avg_session_length', 0),
                    item_feat.get('price', 0),
                    item_feat.get('rating', 0)
                ]
                
                features.append(feature_vector)
                labels.append(data['binary_interactions'].loc[user_id, item_id])
        
        # Train XGBoost
        X = np.array(features)
        y = np.array(labels)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        self.models['xgboost'] = {
            'model': model,
            'user_features': data['user_features'],
            'item_features': data['item_features']
        }
        
        logger.info("XGBoost model trained successfully")
    
    def train_implicit_model(self, data):
        """Train Implicit model for collaborative filtering"""
        logger.info("Training Implicit model...")
        
        interactions = data['binary_interactions']
        
        # Convert to CSR matrix
        from scipy.sparse import csr_matrix
        matrix = csr_matrix(interactions.values)
        
        # Train ALS model
        model = implicit.als.AlternatingLeastSquares(
            factors=50,
            regularization=0.01,
            iterations=50
        )
        
        model.fit(matrix)
        
        self.models['implicit'] = {
            'model': model,
            'interactions': interactions
        }
        
        logger.info("Implicit model trained successfully")
    
    def get_hybrid_recommendations(self, user_id: int, history: List[int], n_recommendations: int = 10):
        """Get hybrid recommendations using multiple models"""
        logger.info(f"Getting hybrid recommendations for user {user_id}")
        
        all_recommendations = {}
        
        # NCF recommendations
        if 'ncf' in self.models:
            ncf_recs = self.get_ncf_recommendations(user_id, history, n_recommendations)
            all_recommendations['ncf'] = ncf_recs
        
        # LightFM recommendations
        if 'lightfm' in self.models:
            lightfm_recs = self.get_lightfm_recommendations(user_id, history, n_recommendations)
            all_recommendations['lightfm'] = lightfm_recs
        
        # XGBoost recommendations
        if 'xgboost' in self.models:
            xgb_recs = self.get_xgboost_recommendations(user_id, history, n_recommendations)
            all_recommendations['xgboost'] = xgb_recs
        
        # Implicit recommendations
        if 'implicit' in self.models:
            implicit_recs = self.get_implicit_recommendations(user_id, history, n_recommendations)
            all_recommendations['implicit'] = implicit_recs
        
        # Combine recommendations using weighted voting
        combined_recommendations = self.combine_recommendations(all_recommendations, n_recommendations)
        
        return combined_recommendations
    
    def get_ncf_recommendations(self, user_id: int, history: List[int], n_recommendations: int):
        """Get recommendations from NCF model"""
        if 'ncf' not in self.models:
            return []
        
        model_data = self.models['ncf']
        model = model_data['model']
        user_to_idx = model_data['user_to_idx']
        item_to_idx = model_data['item_to_idx']
        
        if user_id not in user_to_idx:
            return []
        
        user_idx = user_to_idx[user_id]
        scores = []
        
        model.eval()
        with torch.no_grad():
            for item_id, item_idx in item_to_idx.items():
                if item_id not in history:
                    user_tensor = torch.tensor([user_idx])
                    item_tensor = torch.tensor([item_idx])
                    score = model(user_tensor, item_tensor).item()
                    scores.append((item_id, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    def get_lightfm_recommendations(self, user_id: int, history: List[int], n_recommendations: int):
        """Get recommendations from LightFM model"""
        if 'lightfm' not in self.models:
            return []
        
        model_data = self.models['lightfm']
        model = model_data['model']
        dataset = model_data['dataset']
        
        # Get user internal ID
        user_internal_id = dataset.mapping()[0].get(user_id)
        if user_internal_id is None:
            return []
        
        # Get scores for all items
        scores = model.predict(user_internal_id, np.arange(dataset.num_items))
        
        # Get top recommendations
        top_items = np.argsort(scores)[::-1][:n_recommendations * 2]  # Get more to filter
        
        recommendations = []
        for item_idx in top_items:
            item_id = dataset.mapping()[2][item_idx]
            if item_id not in history:
                recommendations.append((item_id, scores[item_idx]))
                if len(recommendations) >= n_recommendations:
                    break
        
        return recommendations
    
    def get_xgboost_recommendations(self, user_id: int, history: List[int], n_recommendations: int):
        """Get recommendations from XGBoost model"""
        if 'xgboost' not in self.models:
            return []
        
        model_data = self.models['xgboost']
        model = model_data['model']
        user_features = model_data['user_features']
        item_features = model_data['item_features']
        
        user_feat = user_features.get(user_id, {})
        scores = []
        
        for item_id, item_feat in item_features.items():
            if item_id not in history:
                feature_vector = [
                    user_feat.get('total_events', 0),
                    user_feat.get('transaction_count', 0),
                    user_feat.get('avg_session_length', 0),
                    item_feat.get('price', 0),
                    item_feat.get('rating', 0)
                ]
                
                score = model.predict_proba([feature_vector])[0][1]
                scores.append((item_id, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    def get_implicit_recommendations(self, user_id: int, history: List[int], n_recommendations: int):
        """Get recommendations from Implicit model"""
        if 'implicit' not in self.models:
            return []
        
        model_data = self.models['implicit']
        model = model_data['model']
        interactions = model_data['interactions']
        
        if user_id not in interactions.index:
            return []
        
        user_idx = interactions.index.get_loc(user_id)
        scores = model.recommend(user_idx, interactions.values, N=n_recommendations * 2)
        
        recommendations = []
        for item_idx, score in zip(scores[0], scores[1]):
            item_id = interactions.columns[item_idx]
            if item_id not in history:
                recommendations.append((item_id, score))
                if len(recommendations) >= n_recommendations:
                    break
        
        return recommendations
    
    def combine_recommendations(self, all_recommendations: Dict, n_recommendations: int):
        """Combine recommendations from multiple models using weighted voting"""
        item_scores = {}
        model_weights = {'ncf': 0.3, 'lightfm': 0.25, 'xgboost': 0.25, 'implicit': 0.2}
        
        for model_name, recommendations in all_recommendations.items():
            weight = model_weights.get(model_name, 0.1)
            for item_id, score in recommendations:
                if item_id not in item_scores:
                    item_scores[item_id] = 0
                item_scores[item_id] += score * weight
        
        # Sort by combined score
        combined = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        return combined[:n_recommendations]
    
    def get_content_based_recommendations(self, item_id: int, n_recommendations: int = 10):
        """Get content-based recommendations using item features"""
        if not self.sentence_transformer:
            return []
        
        # This would require item descriptions/text features
        # For now, return empty list
        return []
    
    def get_explanation(self, user_id: int, item_id: int, recommendation_score: float):
        """Generate explanation for recommendation"""
        explanations = [
            f"Based on your purchase history, this item has a {recommendation_score:.1%} match score.",
            f"Similar users who bought items like yours also purchased this product.",
            f"This item is frequently bought together with items in your cart.",
            f"Based on your preferences and browsing history, this is a highly recommended item."
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
rec_system = AdvancedRecommendationSystem()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': list(rec_system.models.keys())
    })

@app.route('/train', methods=['POST'])
def train_models():
    """Train all recommendation models"""
    try:
        logger.info("Starting model training...")
        
        # Load and preprocess data
        data = rec_system.load_and_preprocess_data()
        
        # Train all models
        rec_system.train_neural_collaborative_filtering(data)
        rec_system.train_lightfm_model(data)
        rec_system.train_xgboost_model(data)
        rec_system.train_implicit_model(data)
        
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

@app.route('/similar_items/<int:item_id>', methods=['GET'])
def get_similar_items(item_id):
    """Get similar items based on content"""
    try:
        n_similar = request.args.get('n', 10, type=int)
        similar_items = rec_system.get_content_based_recommendations(item_id, n_similar)
        
        return jsonify({
            'item_id': item_id,
            'similar_items': similar_items
        })
    
    except Exception as e:
        logger.error(f"Failed to get similar items: {str(e)}")
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
            'cache_status': 'active' if rec_system.redis_client else 'inactive',
            'sentence_transformer_loaded': rec_system.sentence_transformer is not None,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(analytics)
    
    except Exception as e:
        logger.error(f"Failed to get analytics: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting Advanced ML Recommendation Service...")
    app.run(host='0.0.0.0', port=5001, debug=True)
