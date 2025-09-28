"""
Model management and versioning utilities
"""

import os
import json
import pickle
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages model versions and storage"""
    
    def __init__(self, model_dir: str = "models/checkpoints"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
    def save_model(self, model: Any, version: str, metadata: Dict[str, Any] = None):
        """Save model with version"""
        model_path = os.path.join(self.model_dir, f"model_{version}.pkl")
        metadata_path = os.path.join(self.model_dir, f"metadata_{version}.json")
        
        # Save model
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Save metadata
        if metadata is None:
            metadata = {}
        
        metadata.update({
            'version': version,
            'created_at': datetime.now().isoformat(),
            'model_path': model_path
        })
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved: {version}")
    
    def load_model(self, version: str):
        """Load model by version"""
        model_path = os.path.join(self.model_dir, f"model_{version}.pkl")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model version {version} not found")
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        logger.info(f"Model loaded: {version}")
        return model
    
    def list_models(self):
        """List all available models"""
        models = []
        for file in os.listdir(self.model_dir):
            if file.startswith('metadata_'):
                version = file.replace('metadata_', '').replace('.json', '')
                metadata_path = os.path.join(self.model_dir, file)
                
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                models.append(metadata)
        
        return sorted(models, key=lambda x: x['created_at'], reverse=True)
