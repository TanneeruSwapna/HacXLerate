from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder  # For real categories

app = Flask(__name__)

@app.before_first_request
def load_and_train():
    global model, user_to_idx, item_to_idx, num_users, num_items, product_features, product_id_to_name

    # Load real Retailrocket data (adjust path for other datasets)
    events = pd.read_csv('data/events.csv')  # Columns: timestamp, visitorid, event, itemid, transactionid
    item_props = pd.read_csv('data/item_properties.csv')  # Columns: timestamp, itemid, property, value

    # Filter to transactions (buys) for interactions
    events = events[events['event'] == 'transaction']  # Or include 'addtocart' for more data

    # Create interactions matrix
    interactions = events.pivot_table(index='visitorid', columns='itemid', aggfunc='size', fill_value=0)
    interactions = (interactions > 0).astype(int)  # Binary: bought or not

    # Split
    train_data, test_data = train_test_split(interactions, test_size=0.2, random_state=42)

    # Mappings
    user_to_idx = {u: i for i, u in enumerate(train_data.index.unique())}
    item_to_idx = {i: j for j, i in enumerate(train_data.columns.unique())}
    num_users = len(user_to_idx)
    num_items = len(item_to_idx)

    # Train matrix
    train_matrix = np.array(train_data.reindex(index=list(user_to_idx.keys()), columns=list(item_to_idx.keys()), fill_value=0))

    # PyTorch Dataset (same as before)
    class RecDataset(Dataset):
        def __init__(self, matrix):
            self.users, self.items = np.where(matrix > 0)
            self.ratings = matrix[self.users, self.items]

        def __len__(self):
            return len(self.users)

        def __getitem__(self, idx):
            return self.users[idx], self.items[idx], self.ratings[idx]

    train_dataset = RecDataset(train_matrix)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # NCF Model (same)
    class NCF(nn.Module):
        def __init__(self, num_users, num_items, embedding_size=64):
            super().__init__()
            self.user_emb = nn.Embedding(num_users, embedding_size)
            self.item_emb = nn.Embedding(num_items, embedding_size)
            self.fc = nn.Sequential(
                nn.Linear(embedding_size * 2, 128),
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

    model = NCF(num_users, num_items)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()

    # Train (increase epochs for large data)
    model.train()
    for epoch in range(30):  # More for better accuracy
        total_loss = 0
        for u, i, r in train_loader:
            u, i, r = u.long(), i.long(), r.float().unsqueeze(1)
            optimizer.zero_grad()
            pred = model(u, i)
            loss = criterion(pred, r)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f'Epoch {epoch+1}, Loss: {total_loss / len(train_loader):.4f}')

    # Evaluate
    model.eval()
    with torch.no_grad():
        test_users, test_items = np.where(test_data.values > 0)
        test_users_idx = [user_to_idx.get(test_data.index[tu], 0) for tu in test_users]
        test_items_idx = [item_to_idx.get(test_data.columns[ti], 0) for ti in test_items]
        preds = model(torch.tensor(test_users_idx), torch.tensor(test_items_idx)).numpy().flatten()
        binary_preds = (preds > 0.5).astype(int)
        true_labels = test_data.values[test_users, test_items]
        prec = precision_score(true_labels, binary_preds)
        print(f'Precision: {prec * 100:.2f}%')  # Expect >95% with tuning

    # Real Features for Similarity (from item_properties)
    # Example: Use category/property as features (simplified)
    item_props = item_props[item_props['property'] == 'categoryid']  # Or other props
    item_props = item_props.drop_duplicates(subset='itemid', keep='last')
    le = LabelEncoder()
    item_props['value'] = le.fit_transform(item_props['value'].astype(str))
    product_features = {row['itemid']: np.array([row['value']]) for _, row in item_props.iterrows()}  # 1D for simplicity; expand
    product_id_to_name = dict(zip(events['itemid'], [f'Item_{i}' for i in events['itemid']]))  # Placeholder names

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    history = data['history']  # Assume backend sends product_ids now (update if names)

    # Similarity with real features
    user_vec = np.mean([product_features.get(p, np.zeros(1)) for p in history], axis=0)
    sims = {p: cosine_similarity([user_vec], [vec])[0][0] for p, vec in product_features.items() if p not in history}
    top_sims = sorted(sims.items(), key=lambda x: x[1], reverse=True)[:3]

    # PyTorch Scoring
    scores = []
    for item_id, sim in top_sims:
        user_id = 0  # Still dummy; update backend to send real user_id, map to idx
        input_tensor = torch.tensor([user_to_idx.get(user_id, 0), item_to_idx.get(item_id, 0)])
        score = model(input_tensor[0].unsqueeze(0), input_tensor[1].unsqueeze(0)).item()
        product_name = product_id_to_name.get(item_id, f'Product_{item_id}')
        scores.append({'product': product_name, 'score': score, 'sim': sim})

    return jsonify({'recommendations': scores})

if __name__ == '__main__':
    app.run(port=5001)