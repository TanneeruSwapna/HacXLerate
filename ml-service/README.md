# 🤖 ML Services - B2B Marketplace AI Recommendations

## 📁 **File Organization**

### **Core ML Services**
```
ml-service/
├── core/                          # Core ML algorithms
│   ├── __init__.py
│   ├── base_recommender.py        # Base recommendation class
│   ├── content_based.py           # Content-based filtering
│   ├── collaborative_filtering.py # Collaborative filtering
│   ├── hybrid_recommender.py      # Hybrid approach
│   ├── neural_collaborative.py    # Neural collaborative filtering
├── models/                        # Trained models storage
│   ├── __init__.py
│   ├── model_manager.py           # Model versioning & management
│   ├── model_evaluator.py         # Model performance evaluation
│   └── checkpoints/               # Model checkpoints
├── data/                          # Data processing
│   ├── __init__.py
│   ├── data_loader.py             # Data loading utilities
│   ├── data_preprocessor.py       # Data preprocessing
│   ├── feature_engineering.py     # Feature extraction
│   └── datasets/                  # Raw and processed datasets
├── training/                      # Model training
│   ├── __init__.py
│   ├── trainer.py                 # Training orchestrator
│   ├── hyperparameter_tuner.py    # Hyperparameter optimization
│   ├── cross_validator.py         # Cross-validation
│   └── training_configs/          # Training configurations
├── inference/                     # Model inference
│   ├── __init__.py
│   ├── inference_engine.py        # Real-time inference
│   ├── batch_inference.py         # Batch processing
│   └── recommendation_api.py      # API endpoints
├── monitoring/                    # Model monitoring
│   ├── __init__.py
│   ├── performance_monitor.py     # Performance tracking
│   ├── drift_detector.py          # Data drift detection
│   └── alerts.py                  # Alert system
├── utils/                         # Utilities
│   ├── __init__.py
│   ├── config.py                  # Configuration management
│   ├── logging_config.py          # Logging setup
│   ├── metrics.py                 # Evaluation metrics
│   └── helpers.py                 # Helper functions
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_data_processing.py
│   └── test_inference.py
├── scripts/                       # Utility scripts
│   ├── download_datasets.py       # Download large datasets
│   ├── train_models.py            # Training script
│   ├── evaluate_models.py         # Evaluation script
│   └── deploy_models.py           # Deployment script
├── configs/                       # Configuration files
│   ├── training_config.yaml       # Training parameters
│   ├── model_config.yaml          # Model configurations
│   └── data_config.yaml           # Data configurations
├── requirements.txt               # Python dependencies
├── requirements-full.txt          # Full dependencies for large datasets
├── simple_ml_server.py           # Simple ML server (Python 3.12 compatible)
├── advanced_ml_server.py         # Advanced ML server with all features
├── ml_server.py                  # Original ML server
└── README.md                     # This file
```

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
# Minimal dependencies (Python 3.12 compatible)
pip install -r requirements.txt

# Full dependencies (for large datasets)
pip install -r requirements-full.txt
```

### **2. Download Large Datasets**
```bash
python scripts/download_datasets.py
```

### **3. Train Models**
```bash
python scripts/train_models.py --config configs/training_config.yaml
```

### **4. Start ML Service**
```bash
# Simple version (Python 3.12)
python simple_ml_server.py

# Advanced version (full features)
python advanced_ml_server.py
```

## 📊 **Large Dataset Training**

### **Supported Datasets**
- **Retailrocket**: 2.7M events, 1.4M users, 235K items
- **Amazon Product Data**: 142M reviews, 9.4M products
- **MovieLens**: 25M ratings, 270K users, 45K movies
- **Custom B2B Data**: Your own business data

### **Training Configuration**
```yaml
# configs/training_config.yaml
training:
  batch_size: 1024
  epochs: 100
  learning_rate: 0.001
  validation_split: 0.2
  
models:
  neural_collaborative:
    hidden_layers: [128, 64, 32]
    dropout: 0.2
    regularization: 0.01
  
  content_based:
    similarity_threshold: 0.7
    feature_weights:
      category: 0.4
      brand: 0.3
      price: 0.2
      rating: 0.1
```

### **Performance Optimization**
- **GPU Support**: CUDA acceleration for PyTorch models
- **Distributed Training**: Multi-GPU and multi-node training
- **Memory Optimization**: Efficient data loading and processing
- **Caching**: Redis caching for fast inference

## 🔧 **Model Management**

### **Model Versioning**
```python
from models.model_manager import ModelManager

manager = ModelManager()
manager.save_model(model, version="v1.0")
manager.load_model(version="v1.0")
manager.list_models()
```

### **Model Evaluation**
```python
from models.model_evaluator import ModelEvaluator

evaluator = ModelEvaluator()
metrics = evaluator.evaluate(model, test_data)
print(f"Precision@10: {metrics['precision@10']}")
print(f"Recall@10: {metrics['recall@10']}")
print(f"NDCG@10: {metrics['ndcg@10']}")
```

## 📈 **Monitoring & Analytics**

### **Performance Tracking**
- Real-time model performance metrics
- A/B testing for different models
- User engagement tracking
- Recommendation quality monitoring

### **Data Drift Detection**
- Automatic detection of data distribution changes
- Model retraining triggers
- Performance degradation alerts

## 🧪 **Testing**

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_models.py
python -m pytest tests/test_data_processing.py
```

## 🚀 **Deployment**

### **Production Deployment**
```bash
# Deploy with Docker
docker build -t ml-service .
docker run -p 5001:5001 ml-service

# Deploy with Kubernetes
kubectl apply -f k8s/ml-service.yaml
```

### **Scaling**
- Horizontal scaling with load balancers
- Auto-scaling based on demand
- Model serving optimization

## 📚 **Documentation**

- **API Documentation**: `/docs` endpoint
- **Model Documentation**: In `docs/` folder
- **Training Guides**: In `docs/training/` folder
- **Deployment Guides**: In `docs/deployment/` folder

## 🔗 **Integration**

### **Backend Integration**
```javascript
// Node.js backend calls ML service
const response = await fetch('http://localhost:5001/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 123,
    history: [456, 789],
    n_recommendations: 10
  })
});
```

### **Frontend Integration**
```javascript
// React frontend receives recommendations
const recommendations = await api.getRecommendations(userId);
```

## 🎯 **Next Steps**

1. **Download Large Datasets**: Use `scripts/download_datasets.py`
2. **Train Models**: Use `scripts/train_models.py`
3. **Evaluate Performance**: Use `scripts/evaluate_models.py`
4. **Deploy to Production**: Use `scripts/deploy_models.py`
5. **Monitor Performance**: Use monitoring dashboard

---

**Ready to build enterprise-grade AI recommendations! 🚀**