# Qwipo B2B Marketplace - Personalized Product Recommendations

A comprehensive B2B marketplace platform with AI-powered personalized product recommendations, built for retailers, wholesalers, distributors, and manufacturers.

## 🚀 Features

### Core B2B Marketplace Features
- **Business Profile Management**: Complete business information, preferences, and settings
- **Advanced Product Catalog**: Rich product information with specifications, pricing tiers, and inventory management
- **Smart Shopping Cart**: Bulk pricing, quantity discounts, and business-specific features
- **Analytics Dashboard**: Business insights, spending trends, and performance metrics

### AI-Powered Recommendations
- **Neural Collaborative Filtering**: Deep learning model for personalized recommendations
- **Content-Based Filtering**: Similarity-based suggestions using product features
- **Real-time Updates**: WebSocket integration for live recommendation updates
- **AI Explanations**: Gemini AI integration for recommendation reasoning

### Technical Architecture
- **Frontend**: React 19 with Vite, modern responsive design
- **Backend**: Node.js with Express, MongoDB, JWT authentication
- **ML Service**: Python Flask with PyTorch, scikit-learn
- **Real-time**: Socket.io for live updates
- **Security**: Helmet, CORS, rate limiting, input validation

## 🏗️ Project Structure

```
HacXLerate/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProductCatalog.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   ├── Cart.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── Profile.jsx
│   │   ├── App.jsx          # Main application
│   │   └── App.css          # Comprehensive styling
│   └── package.json
├── backend/                 # Node.js backend API
│   ├── models/             # MongoDB schemas
│   │   ├── User.js         # Enhanced user model
│   │   ├── Product.js      # Rich product model
│   │   └── Cart.js         # Shopping cart model
│   ├── routes/             # API routes
│   │   ├── auth.js
│   │   ├── products.js
│   │   ├── recommendations.js
│   │   ├── cart.js
│   │   ├── dashboard.js
│   │   ├── analytics.js
│   │   └── user.js
│   └── index.js            # Main server file
└── ml-service/             # Python ML service
    ├── ml_server.py        # Flask ML API
    ├── generate_dataset.py # Data generation
    └── requirements.txt    # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- MongoDB
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd HacXLerate
```

2. **Backend Setup**
```bash
cd backend
npm install
cp .env.example .env
# Configure MongoDB URI and other environment variables
npm start
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

4. **ML Service Setup**
```bash
cd ml-service
pip install -r requirements.txt
python ml_server.py
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
MONGODB_URI=mongodb://localhost:27017/qwipo
JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
PORT=5000
```

## 🎯 Key Features Explained

### 1. Enhanced User Model
The user model now includes comprehensive business information:
- Company details and business type
- Industry and business size
- Address and contact information
- User preferences and notification settings
- Purchase history and wishlist
- Credit limits and payment terms

### 2. Rich Product Model
Products include detailed information:
- Basic info (name, description, price, category)
- Specifications (weight, dimensions, material, color)
- Inventory management (quantity, min/max orders, reorder points)
- Pricing tiers (wholesale, retail, bulk discounts)
- Images and tags

### 3. AI-Powered Recommendations
The recommendation system combines:
- **Neural Collaborative Filtering**: Deep learning model trained on user-item interactions
- **Content-Based Filtering**: Cosine similarity using product features
- **Real-time Updates**: WebSocket integration for live recommendations
- **AI Explanations**: Gemini AI provides reasoning for recommendations

### 4. Advanced Frontend Features
- **Responsive Design**: Mobile-first approach with modern UI/UX
- **Real-time Updates**: Live cart updates and notifications
- **Advanced Filtering**: Category, brand, price range, and search filters
- **Analytics Dashboard**: Business insights and performance metrics
- **Profile Management**: Complete business profile editing

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product by ID

### Recommendations
- `GET /api/recommendations` - Get personalized recommendations

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update item quantity
- `DELETE /api/cart/remove` - Remove item from cart

### Dashboard & Analytics
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/analytics` - Get business analytics
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

## 🤖 ML Service

The ML service provides:
- **Neural Collaborative Filtering**: PyTorch-based deep learning model
- **Content-Based Filtering**: Scikit-learn cosine similarity
- **Real Dataset Integration**: Retailrocket dataset support
- **Model Training**: Automatic model training and evaluation

### ML Service Endpoints
- `POST /predict` - Get product recommendations
- `GET /health` - Service health check

## 🎨 Frontend Components

### Dashboard
- Business overview with key metrics
- Quick action buttons
- Recommendation preview
- Real-time updates

### Product Catalog
- Advanced filtering and search
- Grid and list view modes
- Product specifications
- Bulk pricing information

### Recommendations
- AI-powered suggestions
- Score-based filtering
- Detailed explanations
- Real-time updates

### Analytics
- Business performance metrics
- Spending trends
- Category analysis
- Monthly insights

### Profile Management
- Business information editing
- Preference settings
- Notification preferences
- Account management

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Joi schema validation
- **Rate Limiting**: API rate limiting
- **CORS Protection**: Cross-origin resource sharing
- **Helmet Security**: Security headers
- **Password Hashing**: bcryptjs for password security

## 📱 Responsive Design

The application is fully responsive with:
- Mobile-first design approach
- Flexible grid layouts
- Touch-friendly interfaces
- Optimized for all screen sizes

## 🚀 Deployment

### Backend Deployment
```bash
cd backend
npm run build
# Deploy to your preferred platform (Heroku, AWS, etc.)
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy to Vercel, Netlify, or your preferred platform
```

### ML Service Deployment
```bash
cd ml-service
# Deploy to Python hosting platform (Railway, Render, etc.)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- **Advanced Analytics**: More detailed business insights
- **Machine Learning**: Enhanced recommendation algorithms
- **Mobile App**: Native mobile applications
- **Integration**: Third-party service integrations
- **Scalability**: Microservices architecture
- **Performance**: Caching and optimization

---

Built with ❤️ for the B2B marketplace revolution.
