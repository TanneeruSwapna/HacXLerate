"""
Neural Collaborative Filtering for B2B recommendations
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Dict, Any, Tuple
import logging
from .base_recommender import BaseRecommender

logger = logging.getLogger(__name__)

class NCFDataset(Dataset):
    """Dataset for Neural Collaborative Filtering"""
    
    def __init__(self, interactions, item_features, user_features):
        self.interactions = interactions
        self.item_features = item_features
        self.user_features = user_features
        self.samples = self._create_samples()
    
    def _create_samples(self):
        """Create training samples from interactions"""
        samples = []
        for user_id, items in self.interactions.items():
            for item_id, rating in items.items():
                if rating > 0:  # Positive interaction
                    samples.append((user_id, item_id, 1))
                    
                    # Add negative samples
                    neg_item = np.random.choice(list(self.item_features.keys()))
                    while neg_item in items:
                        neg_item = np.random.choice(list(self.item_features.keys()))
                    samples.append((user_id, neg_item, 0))
        
        return samples
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        user_id, item_id, label = self.samples[idx]
        return {
            'user_id': torch.tensor(user_id, dtype=torch.long),
            'item_id': torch.tensor(item_id, dtype=torch.long),
            'label': torch.tensor(label, dtype=torch.float)
        }

class NCFModel(nn.Module):
    """Neural Collaborative Filtering Model"""
    
    def __init__(self, num_users, num_items, embedding_dim=50, hidden_layers=[128, 64, 32]):
        super(NCFModel, self).__init__()
        
        self.num_users = num_users
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        
        # User and item embeddings
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        
        # MLP layers
        self.mlp_layers = nn.ModuleList()
        input_dim = embedding_dim * 2
        
        for hidden_dim in hidden_layers:
            self.mlp_layers.append(nn.Linear(input_dim, hidden_dim))
            self.mlp_layers.append(nn.ReLU())
            self.mlp_layers.append(nn.Dropout(0.2))
            input_dim = hidden_dim
        
        # Output layer
        self.output_layer = nn.Linear(input_dim, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, user_ids, item_ids):
        # Get embeddings
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        # Concatenate embeddings
        concat_emb = torch.cat([user_emb, item_emb], dim=1)
        
        # Pass through MLP
        x = concat_emb
        for layer in self.mlp_layers:
            x = layer(x)
        
        # Output
        output = self.output_layer(x)
        output = self.sigmoid(output)
        
        return output.squeeze()

class NeuralCollaborativeFiltering(BaseRecommender):
    """Neural Collaborative Filtering Recommender"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("NeuralCollaborativeFiltering", config)
        
        self.embedding_dim = self.config.get('embedding_dim', 50)
        self.hidden_layers = self.config.get('hidden_layers', [128, 64, 32])
        self.learning_rate = self.config.get('learning_rate', 0.001)
        self.batch_size = self.config.get('batch_size', 1024)
        self.epochs = self.config.get('epochs', 100)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.model = None
        self.user_mapping = {}
        self.item_mapping = {}
        self.reverse_user_mapping = {}
        self.reverse_item_mapping = {}
    
    def train(self, data: Dict[str, Any]) -> None:
        """Train the NCF model"""
        logger.info("Training Neural Collaborative Filtering model...")
        
        interactions = data['interactions']
        item_features = data['item_features']
        user_features = data['user_features']
        
        # Create mappings
        self._create_mappings(interactions, item_features)
        
        # Prepare data
        dataset = NCFDataset(interactions, item_features, user_features)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        
        # Initialize model
        self.model = NCFModel(
            num_users=len(self.user_mapping),
            num_items=len(self.item_mapping),
            embedding_dim=self.embedding_dim,
            hidden_layers=self.hidden_layers
        ).to(self.device)
        
        # Loss and optimizer
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Training loop
        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0
            for batch in dataloader:
                user_ids = batch['user_id'].to(self.device)
                item_ids = batch['item_id'].to(self.device)
                labels = batch['label'].to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(user_ids, item_ids)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}, Loss: {total_loss/len(dataloader):.4f}")
        
        self.is_trained = True
        logger.info("Neural Collaborative Filtering training completed")
    
    def predict(self, user_id: int, history: List[int], n_recommendations: int = 10) -> List[Tuple[int, float]]:
        """Generate recommendations using NCF model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        self.model.eval()
        with torch.no_grad():
            # Get user index
            if user_id not in self.user_mapping:
                return []
            
            user_idx = self.user_mapping[user_id]
            user_tensor = torch.tensor([user_idx], dtype=torch.long).to(self.device)
            
            # Score all items
            scores = []
            for item_id, item_idx in self.item_mapping.items():
                if item_id not in history:
                    item_tensor = torch.tensor([item_idx], dtype=torch.long).to(self.device)
                    score = self.model(user_tensor, item_tensor).item()
                    scores.append((item_id, score))
            
            # Sort by score and return top recommendations
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:n_recommendations]
    
    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate NCF model performance"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Implementation of evaluation metrics
        # This would include precision@k, recall@k, NDCG@k, etc.
        return {
            'precision@10': 0.0,
            'recall@10': 0.0,
            'ndcg@10': 0.0
        }
    
    def _create_mappings(self, interactions, item_features):
        """Create user and item mappings"""
        # User mapping
        users = set(interactions.keys())
        self.user_mapping = {user_id: idx for idx, user_id in enumerate(users)}
        self.reverse_user_mapping = {idx: user_id for user_id, idx in self.user_mapping.items()}
        
        # Item mapping
        items = set()
        for user_items in interactions.values():
            items.update(user_items.keys())
        items.update(item_features.keys())
        
        self.item_mapping = {item_id: idx for idx, item_id in enumerate(items)}
        self.reverse_item_mapping = {idx: item_id for item_id, idx in self.item_mapping.items()}
