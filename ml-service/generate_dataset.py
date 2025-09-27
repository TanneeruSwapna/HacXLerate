import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Parameters
num_rows = 10000  # Exactly 10,000 rows
num_users = 500
num_products = 2000

# Users
users = np.arange(1, num_users + 1)
user_ids = np.random.choice(users, num_rows)

# Products and categories (inspired by Instacart/Amazon)
categories = ['Electronics', 'Clothing', 'Books', 'Grocery', 'Home', 'Sports']
product_ids = np.arange(1, num_products + 1)
categories_list = np.random.choice(categories, num_products)
product_names = [f'Product_{i}_{cat[:3]}' for i, cat in zip(product_ids, categories_list)]
prices = np.random.uniform(1, 100, num_products)

# Events (from Retailrocket)
event_types = ['view', 'add_to_cart', 'transaction']
events = np.random.choice(event_types, num_rows, p=[0.6, 0.3, 0.1])

# Ratings (from Amazon, only for transactions)
ratings = np.where(events == 'transaction', np.random.randint(1, 6, num_rows), np.nan)

# Quantities (from Instacart, only for transactions)
quantities = np.where(events == 'transaction', np.random.randint(1, 11, num_rows), 1)

# Timestamps (over 2024)
start_date = datetime(2024, 1, 1)
timestamps = [start_date + timedelta(days=np.random.randint(0, 365), hours=np.random.randint(0, 24)) for _ in range(num_rows)]

# Create DataFrame
df = pd.DataFrame({
    'user_id': user_ids,
    'product_id': np.random.choice(product_ids, num_rows),
    'category': np.random.choice(categories, num_rows),
    'product_name': np.random.choice(product_names, num_rows),
    'price': np.random.choice(prices, num_rows),
    'quantity': quantities,
    'event_type': events,
    'rating': ratings,
    'timestamp': timestamps
})

# Sort by timestamp for chronological order
df = df.sort_values('timestamp').reset_index(drop=True)

# Save to CSV
df.to_csv('combined_ecommerce_dataset.csv', index=False)
print(f"Dataset saved! Shape: {df.shape}")
print(df.head(10))  # Preview