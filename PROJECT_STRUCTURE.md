# 🏗️ Complete B2B Marketplace Project Structure

## 📁 **HacXLerate Project Overview**

```
HacXLerate/                                    # Main project directory
├── 📁 frontend/                               # React.js Frontend Application
├── 📁 backend/                                # Node.js Backend API
├── 📁 ml-service/                             # Python ML/AI Service
├── 📁 docs/                                   # Documentation
├── 📁 scripts/                                # Utility scripts
├── 📁 configs/                                # Configuration files
└── 📁 deployment/                             # Deployment configurations
```

---

## 🎨 **Frontend Structure (React.js)**

```
frontend/
├── 📁 public/                                 # Static assets
│   ├── 📄 index.html                         # Main HTML template
│   ├── 📄 favicon.ico                        # Site favicon
│   └── 📁 images/                            # Static images
├── 📁 src/                                   # Source code
│   ├── 📁 components/                        # Reusable UI components
│   │   ├── 📄 Header.jsx                     # Navigation header
│   │   ├── 📄 Footer.jsx                     # Site footer
│   │   ├── 📄 Sidebar.jsx                    # Navigation sidebar
│   │   ├── 📄 LoadingSpinner.jsx             # Loading indicator
│   │   ├── 📄 ErrorBoundary.jsx              # Error handling
│   │   ├── 📄 ProductCard.jsx                # Product display card
│   │   ├── 📄 SearchBar.jsx                  # Search functionality
│   │   ├── 📄 FilterPanel.jsx                # Product filters
│   │   ├── 📄 Pagination.jsx                 # Page navigation
│   │   └── 📄 Modal.jsx                      # Modal dialogs
│   ├── 📁 pages/                             # Page components
│   │   ├── 📄 DashboardPage.jsx              # Main dashboard
│   │   ├── 📄 DashboardPage.css              # Dashboard styles
│   │   ├── 📄 ProductCatalogPage.jsx         # Product catalog
│   │   ├── 📄 ProductCatalogPage.css         # Catalog styles
│   │   ├── 📄 RecommendationsPage.jsx        # AI recommendations
│   │   ├── 📄 RecommendationsPage.css        # Recommendations styles
│   │   ├── 📄 CartPage.jsx                   # Shopping cart
│   │   ├── 📄 CartPage.css                   # Cart styles
│   │   ├── 📄 AnalyticsPage.jsx              # Business analytics
│   │   ├── 📄 AnalyticsPage.css              # Analytics styles
│   │   ├── 📄 ProfilePage.jsx                # User profile
│   │   ├── 📄 ProfilePage.css                # Profile styles
│   │   ├── 📄 LoginPage.jsx                  # User login
│   │   ├── 📄 LoginPage.css                  # Login styles
│   │   ├── 📄 RegisterPage.jsx               # User registration
│   │   └── 📄 RegisterPage.css               # Registration styles
│   ├── 📁 styles/                            # Global styles
│   │   ├── 📄 global.css                     # Global CSS variables
│   │   ├── 📄 components.css                 # Component styles
│   │   └── 📄 utilities.css                  # Utility classes
│   ├── 📁 hooks/                             # Custom React hooks
│   │   ├── 📄 useAuth.js                     # Authentication hook
│   │   ├── 📄 useCart.js                     # Cart management hook
│   │   ├── 📄 useRecommendations.js          # Recommendations hook
│   │   └── 📄 useAnalytics.js                # Analytics hook
│   ├── 📁 services/                          # API services
│   │   ├── 📄 api.js                         # Main API client
│   │   ├── 📄 authService.js                 # Authentication API
│   │   ├── 📄 productService.js              # Product API
│   │   ├── 📄 cartService.js                 # Cart API
│   │   ├── 📄 recommendationService.js       # ML recommendations API
│   │   └── 📄 analyticsService.js            # Analytics API
│   ├── 📁 utils/                             # Utility functions
│   │   ├── 📄 constants.js                   # App constants
│   │   ├── 📄 helpers.js                     # Helper functions
│   │   ├── 📄 validators.js                  # Form validation
│   │   └── 📄 formatters.js                  # Data formatters
│   ├── 📁 context/                           # React Context
│   │   ├── 📄 AuthContext.js                 # Authentication context
│   │   ├── 📄 CartContext.js                 # Cart context
│   │   └── 📄 ThemeContext.js                # Theme context
│   ├── 📄 App.jsx                            # Main app component
│   ├── 📄 App.css                            # App styles
│   ├── 📄 main.jsx                           # App entry point
│   └── 📄 index.css                          # Global styles
├── 📄 package.json                           # Dependencies & scripts
├── 📄 vite.config.js                         # Vite configuration
├── 📄 .env                                   # Environment variables
├── 📄 .gitignore                             # Git ignore rules
└── 📄 README.md                              # Frontend documentation
```

---

## 🔧 **Backend Structure (Node.js)**

```
backend/
├── 📁 routes/                                # API routes
│   ├── 📄 index.js                           # Main route handler
│   ├── 📄 auth.js                            # Authentication routes
│   ├── 📄 products.js                        # Product management routes
│   ├── 📄 cart.js                            # Cart management routes
│   ├── 📄 recommendations.js                 # ML recommendations routes
│   ├── 📄 analytics.js                       # Analytics routes
│   ├── 📄 dashboard.js                       # Dashboard routes
│   ├── 📄 user.js                            # User management routes
│   └── 📄 orders.js                          # Order management routes
├── 📁 models/                                # Database models
│   ├── 📄 User.js                            # User schema
│   ├── 📄 Product.js                         # Product schema
│   ├── 📄 Cart.js                            # Cart schema
│   ├── 📄 Order.js                           # Order schema
│   ├── 📄 Category.js                        # Category schema
│   ├── 📄 Review.js                          # Review schema
│   └── 📄 index.js                           # Model exports
├── 📁 controllers/                           # Business logic
│   ├── 📄 authController.js                  # Authentication logic
│   ├── 📄 productController.js               # Product logic
│   ├── 📄 cartController.js                  # Cart logic
│   ├── 📄 recommendationController.js        # ML integration logic
│   ├── 📄 analyticsController.js             # Analytics logic
│   └── 📄 userController.js                  # User logic
├── 📁 middleware/                            # Custom middleware
│   ├── 📄 auth.js                            # Authentication middleware
│   ├── 📄 validation.js                      # Request validation
│   ├── 📄 rateLimiting.js                    # Rate limiting
│   ├── 📄 errorHandler.js                    # Error handling
│   └── 📄 logging.js                         # Request logging
├── 📁 services/                              # External services
│   ├── 📄 mlService.js                       # ML service integration
│   ├── 📄 emailService.js                    # Email service
│   ├── 📄 paymentService.js                  # Payment processing
│   └── 📄 notificationService.js             # Notifications
├── 📁 utils/                                 # Utility functions
│   ├── 📄 database.js                        # Database connection
│   ├── 📄 jwt.js                             # JWT utilities
│   ├── 📄 encryption.js                      # Encryption utilities
│   ├── 📄 validation.js                      # Validation utilities
│   └── 📄 logger.js                          # Logging utilities
├── 📁 config/                                # Configuration
│   ├── 📄 database.js                        # Database config
│   ├── 📄 redis.js                           # Redis config
│   └── 📄 environment.js                     # Environment config
├── 📁 tests/                                 # Test files
│   ├── 📄 auth.test.js                       # Auth tests
│   ├── 📄 products.test.js                   # Product tests
│   ├── 📄 cart.test.js                       # Cart tests
│   └── 📄 recommendations.test.js            # ML integration tests
├── 📄 index.js                               # Main server file
├── 📄 package.json                           # Dependencies & scripts
├── 📄 .env                                   # Environment variables
├── 📄 .gitignore                             # Git ignore rules
└── 📄 README.md                              # Backend documentation
```

---

## 🤖 **ML Service Structure (Python)**

```
ml-service/
├── 📁 core/                                  # Core ML algorithms
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 base_recommender.py                # Base recommendation class
│   ├── 📄 content_based.py                   # Content-based filtering
│   ├── 📄 collaborative_filtering.py         # Collaborative filtering
│   ├── 📄 hybrid_recommender.py              # Hybrid approach
│   └── 📄 neural_collaborative.py            # Neural collaborative filtering
├── 📁 models/                                # Trained models storage
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 model_manager.py                   # Model versioning & management
│   ├── 📄 model_evaluator.py                 # Model performance evaluation
│   └── 📁 checkpoints/                       # Model checkpoints
│       ├── 📄 ncf_model.pth                  # Neural CF model
│       ├── 📄 content_based_model.pkl        # Content-based model
│       ├── 📄 collaborative_model.pkl        # Collaborative model
│       └── 📄 hybrid_model.pkl               # Hybrid model
├── 📁 data/                                  # Data processing
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 data_loader.py                     # Data loading utilities
│   ├── 📄 data_preprocessor.py               # Data preprocessing
│   ├── 📄 feature_engineering.py             # Feature extraction
│   └── 📁 datasets/                          # Raw and processed datasets
│       ├── 📄 b2b_products.csv               # B2B product data
│       ├── 📄 b2b_users.csv                  # B2B user data
│       ├── 📄 b2b_transactions.csv           # B2B transaction data
│       ├── 📄 retailrocket_events.csv        # Retailrocket events
│       ├── 📄 retailrocket_item_properties.csv # Retailrocket items
│       ├── 📄 amazon_products.csv            # Amazon products
│       ├── 📄 amazon_reviews.csv             # Amazon reviews
│       ├── 📄 movielens_movies.csv           # MovieLens movies
│       └── 📄 movielens_ratings.csv          # MovieLens ratings
├── 📁 training/                              # Model training
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 trainer.py                         # Training orchestrator
│   ├── 📄 hyperparameter_tuner.py            # Hyperparameter optimization
│   ├── 📄 cross_validator.py                 # Cross-validation
│   └── 📁 training_configs/                  # Training configurations
│       ├── 📄 ncf_config.yaml                # NCF training config
│       ├── 📄 content_based_config.yaml      # Content-based config
│       └── 📄 collaborative_config.yaml      # Collaborative config
├── 📁 inference/                             # Model inference
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 inference_engine.py                # Real-time inference
│   ├── 📄 batch_inference.py                 # Batch processing
│   └── 📄 recommendation_api.py              # API endpoints
├── 📁 monitoring/                            # Model monitoring
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 performance_monitor.py             # Performance tracking
│   ├── 📄 drift_detector.py                  # Data drift detection
│   └── 📄 alerts.py                          # Alert system
├── 📁 utils/                                 # Utilities
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 config.py                          # Configuration management
│   ├── 📄 logging_config.py                  # Logging setup
│   ├── 📄 metrics.py                         # Evaluation metrics
│   └── 📄 helpers.py                         # Helper functions
├── 📁 tests/                                 # Test suite
│   ├── 📄 __init__.py                        # Package initialization
│   ├── 📄 test_models.py                     # Model tests
│   ├── 📄 test_data_processing.py            # Data processing tests
│   ├── 📄 test_inference.py                  # Inference tests
│   └── 📄 test_training.py                   # Training tests
├── 📁 scripts/                               # Utility scripts
│   ├── 📄 download_datasets.py               # Download large datasets
│   ├── 📄 train_models.py                    # Training script
│   ├── 📄 evaluate_models.py                 # Evaluation script
│   ├── 📄 deploy_models.py                   # Deployment script
│   └── 📄 test_ml_service.py                 # ML service testing
├── 📁 configs/                               # Configuration files
│   ├── 📄 training_config.yaml               # Training parameters
│   ├── 📄 model_config.yaml                  # Model configurations
│   ├── 📄 data_config.yaml                   # Data configurations
│   └── 📄 deployment_config.yaml             # Deployment config
├── 📄 simple_ml_server.py                    # Simple ML server (Python 3.12)
├── 📄 advanced_ml_server.py                  # Advanced ML server
├── 📄 ml_server.py                           # Original ML server
├── 📄 requirements.txt                       # Python dependencies
├── 📄 requirements-full.txt                  # Full dependencies
├── 📄 minimal_requirements.txt               # Minimal dependencies
├── 📄 .env                                   # Environment variables
├── 📄 .gitignore                             # Git ignore rules
└── 📄 README.md                              # ML service documentation
```

---

## 📚 **Documentation Structure**

```
docs/
├── 📄 README.md                              # Main documentation
├── 📁 api/                                   # API documentation
│   ├── 📄 backend-api.md                     # Backend API docs
│   ├── 📄 ml-api.md                          # ML service API docs
│   └── 📄 frontend-api.md                    # Frontend API docs
├── 📁 deployment/                            # Deployment guides
│   ├── 📄 docker.md                          # Docker deployment
│   ├── 📄 kubernetes.md                      # Kubernetes deployment
│   └── 📄 aws.md                             # AWS deployment
├── 📁 development/                           # Development guides
│   ├── 📄 setup.md                           # Development setup
│   ├── 📄 contributing.md                    # Contribution guide
│   └── 📄 testing.md                         # Testing guide
└── 📁 architecture/                          # Architecture docs
    ├── 📄 system-design.md                   # System design
    ├── 📄 database-schema.md                 # Database schema
    └── 📄 ml-pipeline.md                     # ML pipeline
```

---

## 🚀 **Scripts Structure**

```
scripts/
├── 📄 run_all_services.py                    # Master startup script
├── 📄 start_frontend.py                      # Frontend startup
├── 📄 start_backend.py                       # Backend startup
├── 📄 start_ml_service.py                    # ML service startup
├── 📄 test_connection.py                     # Service connection test
├── 📄 setup_environment.py                   # Environment setup
├── 📄 backup_database.py                     # Database backup
├── 📄 migrate_database.py                    # Database migration
├── 📄 deploy_production.py                   # Production deployment
├── 📄 monitor_services.py                    # Service monitoring
├── 📄 start_all.bat                          # Windows batch file
├── 📄 start_all.sh                           # Linux/Mac shell script
├── 📄 QUICK_START.md                         # Quick start guide
├── 📄 HOW_TO_RUN.md                          # How to run guide
├── 📄 STARTUP_GUIDE.md                       # Detailed startup guide
└── 📄 PROJECT_STRUCTURE.md                   # This file
```

---

## ⚙️ **Configuration Structure**

```
configs/
├── 📄 development.yaml                       # Development config
├── 📄 staging.yaml                           # Staging config
├── 📄 production.yaml                        # Production config
├── 📄 docker-compose.yml                     # Docker compose
├── 📄 docker-compose.dev.yml                 # Development Docker
├── 📄 docker-compose.prod.yml                # Production Docker
├── 📄 nginx.conf                             # Nginx configuration
├── 📄 redis.conf                             # Redis configuration
└── 📄 mongodb.conf                           # MongoDB configuration
```

---

## 🚀 **Deployment Structure**

```
deployment/
├── 📁 docker/                                # Docker configurations
│   ├── 📄 Dockerfile.frontend                # Frontend Dockerfile
│   ├── 📄 Dockerfile.backend                 # Backend Dockerfile
│   ├── 📄 Dockerfile.ml-service              # ML service Dockerfile
│   └── 📄 docker-compose.yml                 # Docker compose
├── 📁 kubernetes/                            # Kubernetes configurations
│   ├── 📄 namespace.yaml                     # K8s namespace
│   ├── 📄 frontend-deployment.yaml           # Frontend deployment
│   ├── 📄 backend-deployment.yaml            # Backend deployment
│   ├── 📄 ml-service-deployment.yaml         # ML service deployment
│   ├── 📄 services.yaml                      # K8s services
│   └── 📄 ingress.yaml                       # Ingress configuration
├── 📁 aws/                                   # AWS configurations
│   ├── 📄 cloudformation.yaml                # CloudFormation template
│   ├── 📄 ecs-task-definition.json           # ECS task definition
│   └── 📄 lambda-functions/                  # Lambda functions
└── 📁 terraform/                             # Terraform configurations
    ├── 📄 main.tf                            # Main Terraform config
    ├── 📄 variables.tf                       # Variables
    └── 📄 outputs.tf                         # Outputs
```

---

## 📊 **Key Features by Service**

### **Frontend (React.js)**
- ✅ Modern React 18 with Vite
- ✅ Responsive design with CSS modules
- ✅ State management with Context API
- ✅ Real-time updates with WebSocket
- ✅ Progressive Web App (PWA) support
- ✅ Accessibility (WCAG 2.1)

### **Backend (Node.js)**
- ✅ RESTful API with Express.js
- ✅ MongoDB with Mongoose ODM
- ✅ JWT authentication
- ✅ Rate limiting and security
- ✅ Real-time communication
- ✅ Comprehensive logging

### **ML Service (Python)**
- ✅ Multiple recommendation algorithms
- ✅ Large dataset training support
- ✅ Model versioning and management
- ✅ Real-time inference
- ✅ Performance monitoring
- ✅ A/B testing capabilities

---

## 🔗 **Service Communication**

```
Frontend (Port 3000) ←→ Backend (Port 5000) ←→ ML Service (Port 5001)
     ↓                        ↓                        ↓
  React App              Node.js API              Python ML
  WebSocket              MongoDB                  Redis Cache
  Context API            JWT Auth                 Model Serving
```

---

## 🎯 **Quick Start Commands**

```bash
# Install dependencies
npm install                    # Frontend
npm install                    # Backend  
pip install -r requirements.txt # ML Service

# Start services
npm run dev                    # Frontend
npm start                      # Backend
python simple_ml_server.py     # ML Service

# Or use the master script
python run_all_services.py     # All services
```

---

**This structure provides a complete, scalable B2B marketplace with AI-powered recommendations! 🚀**
