# 🚀 Complete Training Guide for B2B Marketplace ML Models

## 📋 **Overview**

This guide provides step-by-step instructions for training ML models with large datasets to achieve high accuracy and correct recommendations for your B2B marketplace.

## 🎯 **Training Objectives**

- **High Accuracy**: Achieve >85% precision@10 and recall@10
- **Scalability**: Handle datasets with millions of interactions
- **Real-time Performance**: Serve recommendations in <100ms
- **Business Relevance**: Provide meaningful B2B recommendations

---

## 📊 **Step 1: Download Large Datasets**

### **Available Datasets**

1. **Custom B2B Dataset** (Recommended)
   - 5,000 products across 7 categories
   - 2,000 business users
   - 25,000 transactions
   - Realistic B2B features

2. **Retailrocket Dataset**
   - 2.7M events
   - 1.4M users
   - 235K items
   - E-commerce interactions

3. **Amazon Dataset**
   - 142M reviews
   - 9.4M products
   - Rich product metadata

4. **MovieLens Dataset**
   - 25M ratings
   - 270K users
   - 45K movies

### **Download Commands**

```bash
# Download all datasets
cd ml-service
python scripts/download_datasets.py

# Download specific dataset
python scripts/download_datasets.py custom_b2b
python scripts/download_datasets.py retailrocket
python scripts/download_datasets.py amazon
python scripts/download_datasets.py movielens
```

---

## 🏗️ **Step 2: Install Dependencies**

### **Option A: Minimal Setup (Python 3.12 Compatible)**
```bash
cd ml-service
pip install -r minimal_requirements.txt
```

### **Option B: Full Setup (Advanced Features)**
```bash
cd ml-service
pip install -r requirements-full.txt
```

### **Option C: GPU Support (For Large Models)**
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install -r requirements-full.txt
```

---

## ⚙️ **Step 3: Configure Training**

### **Training Configuration**

Edit `ml-service/configs/training_config.yaml`:

```yaml
# Data Configuration
data:
  dataset: "custom_b2b"  # or "retailrocket", "amazon", "movielens"
  batch_size: 1024
  validation_split: 0.2

# Model Configurations
models:
  neural_collaborative:
    enabled: true
    embedding_dim: 50
    hidden_layers: [128, 64, 32]
    learning_rate: 0.001
    epochs: 100
    batch_size: 1024
    
  content_based:
    enabled: true
    similarity_threshold: 0.7
    
  collaborative_filtering:
    enabled: true
    similarity_metric: "cosine"
    
  hybrid:
    enabled: true
    model_weights:
      neural_collaborative: 0.4
      content_based: 0.3
      collaborative_filtering: 0.3

# Training Configuration
training:
  save_models: true
  model_dir: "models/checkpoints"
  evaluate_models: true
```

---

## 🚀 **Step 4: Train Models**

### **Basic Training**
```bash
cd ml-service
python scripts/train_models.py
```

### **Advanced Training Options**
```bash
# Train with specific dataset
python scripts/train_models.py --dataset custom_b2b

# Train specific models
python scripts/train_models.py --models neural_collaborative content_based

# Custom configuration
python scripts/train_models.py --config configs/custom_config.yaml
```

### **Training with Large Datasets**
```bash
# For large datasets, increase batch size and epochs
python scripts/train_models.py --config configs/large_dataset_config.yaml
```

---

## 📊 **Step 5: Evaluate Models**

### **Run Evaluation**
```bash
cd ml-service
python scripts/evaluate_models.py
```

### **Evaluation Metrics**

The evaluation will provide:

- **Precision@10**: Accuracy of top 10 recommendations
- **Recall@10**: Coverage of relevant items
- **NDCG@10**: Ranking quality
- **Coverage**: Percentage of items that can be recommended
- **Diversity**: Variety in recommendations
- **Novelty**: Recommendation of less popular items

### **Expected Results**

| Model | Precision@10 | Recall@10 | NDCG@10 | Coverage |
|-------|-------------|-----------|---------|----------|
| Neural Collaborative | 0.85+ | 0.80+ | 0.82+ | 0.70+ |
| Content-Based | 0.75+ | 0.70+ | 0.75+ | 0.85+ |
| Collaborative Filtering | 0.80+ | 0.75+ | 0.78+ | 0.65+ |
| Hybrid | 0.88+ | 0.85+ | 0.86+ | 0.80+ |

---

## 🔧 **Step 6: Optimize Performance**

### **Hyperparameter Tuning**
```bash
# Enable hyperparameter tuning in config
python scripts/train_models.py --config configs/tuning_config.yaml
```

### **GPU Acceleration**
```bash
# Use GPU for training
export CUDA_VISIBLE_DEVICES=0
python scripts/train_models.py --config configs/gpu_config.yaml
```

### **Distributed Training**
```bash
# Multi-GPU training
export CUDA_VISIBLE_DEVICES=0,1,2,3
python scripts/train_models.py --config configs/distributed_config.yaml
```

---

## 📈 **Step 7: Monitor Training**

### **Real-time Monitoring**
```bash
# Start monitoring dashboard
cd ml-service
python analytics_dashboard.py
```

Access dashboard at: http://localhost:5002

### **Training Logs**
```bash
# View training logs
tail -f logs/training.log

# Monitor GPU usage
nvidia-smi -l 1
```

---

## 🚀 **Step 8: Deploy Models**

### **Start ML Service**
```bash
# Simple version (Python 3.12)
python simple_ml_server.py

# Advanced version (full features)
python advanced_ml_server.py
```

### **Test Recommendations**
```bash
# Test API endpoints
python test_ml_service.py

# Test with real data
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "history": [123, 456], "n_recommendations": 10}'
```

---

## 🔄 **Step 9: Continuous Training**

### **Automated Retraining**
```bash
# Schedule retraining
crontab -e

# Add daily retraining at 2 AM
0 2 * * * cd /path/to/ml-service && python scripts/train_models.py
```

### **A/B Testing**
```bash
# Enable A/B testing in config
python scripts/train_models.py --config configs/ab_testing_config.yaml
```

---

## 📊 **Step 10: Performance Monitoring**

### **Model Performance Tracking**
```bash
# Monitor model performance
python scripts/monitor_models.py

# Generate performance reports
python scripts/generate_report.py
```

### **Data Drift Detection**
```bash
# Detect data drift
python scripts/detect_drift.py

# Retrain if drift detected
python scripts/auto_retrain.py
```

---

## 🎯 **Best Practices**

### **Data Quality**
- ✅ Clean and preprocess data
- ✅ Handle missing values
- ✅ Remove outliers
- ✅ Validate data integrity

### **Model Selection**
- ✅ Start with simple models
- ✅ Use ensemble methods
- ✅ Validate on holdout data
- ✅ Monitor for overfitting

### **Performance Optimization**
- ✅ Use appropriate batch sizes
- ✅ Implement early stopping
- ✅ Use learning rate scheduling
- ✅ Monitor GPU memory usage

### **Production Deployment**
- ✅ Version control models
- ✅ Implement rollback mechanisms
- ✅ Monitor model performance
- ✅ Set up alerts for failures

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Out of Memory**
   ```bash
   # Reduce batch size
   batch_size: 512  # instead of 1024
   ```

2. **Slow Training**
   ```bash
   # Use GPU
   export CUDA_VISIBLE_DEVICES=0
   
   # Increase workers
   n_jobs: -1
   ```

3. **Poor Performance**
   ```bash
   # Increase model complexity
   hidden_layers: [256, 128, 64]
   
   # More training data
   epochs: 200
   ```

4. **Python 3.12 Issues**
   ```bash
   # Use simple ML server
   python simple_ml_server.py
   
   # Or downgrade Python
   conda install python=3.11
   ```

---

## 📚 **Additional Resources**

### **Documentation**
- [ML Service README](ml-service/README.md)
- [API Documentation](docs/api/ml-api.md)
- [Model Architecture](docs/architecture/ml-pipeline.md)

### **Scripts**
- [Download Datasets](ml-service/scripts/download_datasets.py)
- [Train Models](ml-service/scripts/train_models.py)
- [Evaluate Models](ml-service/scripts/evaluate_models.py)

### **Configuration**
- [Training Config](ml-service/configs/training_config.yaml)
- [Model Config](ml-service/configs/model_config.yaml)
- [Data Config](ml-service/configs/data_config.yaml)

---

## 🎉 **Success Criteria**

Your training is successful when:

- ✅ **Precision@10 > 85%**: High accuracy recommendations
- ✅ **Recall@10 > 80%**: Good coverage of relevant items
- ✅ **NDCG@10 > 82%**: High ranking quality
- ✅ **Coverage > 70%**: Most items can be recommended
- ✅ **Response Time < 100ms**: Fast real-time inference
- ✅ **Model Size < 100MB**: Efficient model storage

---

**Ready to build enterprise-grade AI recommendations! 🚀**
