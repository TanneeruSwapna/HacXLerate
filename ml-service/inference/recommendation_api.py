"""
Recommendation API endpoints
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class RecommendationAPI:
    """API endpoints for recommendations"""
    
    def __init__(self, inference_engine):
        self.inference_engine = inference_engine
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/predict', methods=['POST'])
        def predict():
            """Get recommendations for a user"""
            try:
                data = request.json
                user_id = data.get('user_id')
                history = data.get('history', [])
                n_recommendations = data.get('n_recommendations', 10)
                model_name = data.get('model_name', 'hybrid')
                
                if user_id is None:
                    return jsonify({'error': 'user_id is required'}), 400
                
                recommendations = self.inference_engine.get_recommendations(
                    user_id, history, n_recommendations, model_name
                )
                
                return jsonify({
                    'user_id': user_id,
                    'recommendations': recommendations,
                    'model': model_name
                })
                
            except Exception as e:
                logger.error(f"Prediction error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/batch_predict', methods=['POST'])
        def batch_predict():
            """Get batch recommendations"""
            try:
                data = request.json
                requests = data.get('requests', [])
                
                if not requests:
                    return jsonify({'error': 'requests are required'}), 400
                
                results = self.inference_engine.get_batch_recommendations(requests)
                
                return jsonify({
                    'results': results,
                    'count': len(results)
                })
                
            except Exception as e:
                logger.error(f"Batch prediction error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'models': list(self.inference_engine.models.keys()),
                'cache_stats': self.inference_engine.get_cache_stats()
            })
        
        @self.app.route('/cache/clear', methods=['POST'])
        def clear_cache():
            """Clear recommendation cache"""
            self.inference_engine.clear_cache()
            return jsonify({'status': 'cache cleared'})
    
    def run(self, host='0.0.0.0', port=5001, debug=False):
        """Run the API server"""
        logger.info(f"Starting recommendation API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
