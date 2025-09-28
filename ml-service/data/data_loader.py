"""
Data loading utilities
"""

import pandas as pd
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Loads and processes datasets"""
    
    def __init__(self, data_dir: str = "data/datasets"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def load_b2b_dataset(self) -> Dict[str, Any]:
        """Load B2B dataset"""
        try:
            products = pd.read_csv(f"{self.data_dir}/b2b_products.csv")
            users = pd.read_csv(f"{self.data_dir}/b2b_users.csv")
            transactions = pd.read_csv(f"{self.data_dir}/b2b_transactions.csv")
            
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
            
            return {
                'interactions': interactions,
                'item_features': item_features,
                'user_features': user_features,
                'products': products,
                'users': users,
                'transactions': transactions
            }
            
        except Exception as e:
            logger.error(f"Failed to load B2B dataset: {e}")
            return {}
    
    def load_retailrocket_dataset(self) -> Dict[str, Any]:
        """Load Retailrocket dataset"""
        try:
            events = pd.read_csv(f"{self.data_dir}/retailrocket_events.csv")
            item_properties = pd.read_csv(f"{self.data_dir}/retailrocket_item_properties.csv")
            
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
            
            return {
                'interactions': interactions,
                'item_features': item_features,
                'user_features': {},
                'events': events,
                'item_properties': item_properties
            }
            
        except Exception as e:
            logger.error(f"Failed to load Retailrocket dataset: {e}")
            return {}
